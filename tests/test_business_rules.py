import os
import sqlite3
import tempfile
import unittest
from contextlib import closing, contextmanager
from datetime import date, datetime
from unittest.mock import patch
from zoneinfo import ZoneInfo


TARIFAS = {
    "hora_moto": 1500,
    "hora_carro": 3000,
    "minutos_gracia": 10
}


class ConnectionTests(unittest.TestCase):

    def test_conexion_confirma_revierte_y_cierra(self):
        from flask import Flask
        from app.repositories.connection import conectar

        handle, path = tempfile.mkstemp(suffix=".db")
        os.close(handle)

        flask_app = Flask(__name__)
        flask_app.config["DATABASE_PATH"] = path

        try:
            with flask_app.app_context():
                with conectar() as conn:
                    conn.execute("CREATE TABLE prueba(valor INTEGER)")

                with conectar() as conn:
                    conn.execute("INSERT INTO prueba(valor) VALUES (1)")

                with self.assertRaises(RuntimeError):
                    with conectar() as conn:
                        conn.execute("INSERT INTO prueba(valor) VALUES (2)")
                        raise RuntimeError("forzar rollback")

                with conectar() as conn:
                    valores = conn.execute(
                        "SELECT valor FROM prueba ORDER BY valor"
                    ).fetchall()

            self.assertEqual(
                [row[0] for row in valores],
                [1]
            )
        finally:
            os.remove(path)


class CalculosTests(unittest.TestCase):

    def calcular(self, ingreso, salida, minutos_gracia=10):
        from app.utils.calculos import calcular_valor

        tarifas = {
            **TARIFAS,
            "minutos_gracia": minutos_gracia
        }

        with patch(
            "app.utils.calculos.obtener_tarifa_activa",
            return_value=tarifas
        ):
            return calcular_valor("Moto", ingreso, salida)[0]

    def test_hora_exacta_con_gracia_cero_no_cobra_hora_adicional(self):
        ingreso = datetime(2026, 6, 29, 8, 0, tzinfo=ZoneInfo("America/Bogota"))
        salida = datetime(2026, 6, 29, 9, 0, tzinfo=ZoneInfo("America/Bogota"))

        self.assertEqual(self.calcular(ingreso, salida, 0), 1500)

    def test_limite_de_gracia_no_redondea_hacia_arriba(self):
        ingreso = datetime(2026, 6, 29, 8, 0, tzinfo=ZoneInfo("America/Bogota"))
        salida = datetime(2026, 6, 29, 9, 10, tzinfo=ZoneInfo("America/Bogota"))

        self.assertEqual(self.calcular(ingreso, salida, 10), 1500)

    def test_superar_gracia_cobra_hora_adicional(self):
        ingreso = datetime(2026, 6, 29, 8, 0, tzinfo=ZoneInfo("America/Bogota"))
        salida = datetime(2026, 6, 29, 9, 11, tzinfo=ZoneInfo("America/Bogota"))

        self.assertEqual(self.calcular(ingreso, salida, 10), 3000)

    def test_rechaza_hora_de_ingreso_futura(self):
        ingreso = datetime(2026, 6, 29, 10, 0, tzinfo=ZoneInfo("America/Bogota"))
        salida = datetime(2026, 6, 29, 9, 0, tzinfo=ZoneInfo("America/Bogota"))

        with self.assertRaisesRegex(ValueError, "futuro"):
            self.calcular(ingreso, salida)


class TarifasTests(unittest.TestCase):

    def test_rechaza_tarifas_negativas(self):
        from app.services.tarifas_service import actualizar_tarifas

        with patch(
            "app.services.tarifas_service.actualizar_tarifas_db"
        ) as guardar:
            with self.assertRaisesRegex(ValueError, "mayores que cero"):
                actualizar_tarifas(
                    -1, 3000, 10000, 20000,
                    5000, 10000, 50000, 100000, 10
                )

        guardar.assert_not_called()

    def test_rechaza_gracia_mayor_a_59(self):
        from app.services.tarifas_service import actualizar_tarifas

        with self.assertRaisesRegex(ValueError, "entre 0 y 59"):
            actualizar_tarifas(
                1500, 3000, 10000, 20000,
                5000, 10000, 50000, 100000, 60
            )


class MensualidadesTests(unittest.TestCase):

    def test_busqueda_activa_incluye_fecha_actual(self):
        import app.services.mensualidades_service as service

        with patch.object(
            service,
            "_hoy_colombia",
            return_value=date(2026, 6, 29)
        ), patch.object(
            service,
            "buscar_mensualidad_activa_db",
            return_value={"id": 1}
        ) as buscar:
            resultado = service.buscar_mensualidad_activa("abc123")

        buscar.assert_called_once_with("ABC123", "2026-06-29")
        self.assertEqual(resultado["id"], 1)

    def test_rechaza_rango_de_fechas_invertido(self):
        import app.services.mensualidades_service as service

        with patch.object(service, "crear_mensualidad_db") as guardar:
            with self.assertRaisesRegex(ValueError, "inicial"):
                service.crear_mensualidad(
                    "ABC123",
                    "Moto",
                    "Propietario",
                    "3000000000",
                    "2026-07-01",
                    "2026-06-01",
                    "Activa"
                )

        guardar.assert_not_called()


class CierresTests(unittest.TestCase):

    def test_servicio_recalcula_total_general(self):
        import app.services.cierre_service as service

        with patch.object(service, "guardar_cierre_db") as guardar:
            service.guardar_cierre(
                "2026-06-29",
                10000,
                5000,
                999999,
                "  Sin novedades  ",
                "operador",
                "18:00:00"
            )

        guardar.assert_called_once_with(
            "2026-06-29",
            10000,
            5000,
            15000,
            "Sin novedades",
            "operador",
            "18:00:00"
        )

    def test_repositorio_detecta_cierre_en_formato_legacy(self):
        import app.repositories.cierre_repository as repository

        handle, path = tempfile.mkstemp(suffix=".db")
        os.close(handle)

        try:
            with closing(sqlite3.connect(path)) as conn:
                conn.execute("""
                    CREATE TABLE cierres_caja(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        fecha TEXT NOT NULL,
                        total_parqueadero INTEGER NOT NULL,
                        total_lavadero INTEGER NOT NULL,
                        total_general INTEGER NOT NULL,
                        observaciones TEXT,
                        usuario TEXT NOT NULL,
                        hora_cierre TEXT NOT NULL
                    )
                """)
                conn.execute("""
                    INSERT INTO cierres_caja(
                        fecha, total_parqueadero, total_lavadero,
                        total_general, observaciones, usuario, hora_cierre
                    ) VALUES ('29/06/2026', 100, 200, 300, '', 'admin', '18:00:00')
                """)
                conn.commit()

            @contextmanager
            def conectar_prueba():
                with closing(sqlite3.connect(path)) as conn:
                    with conn:
                        yield conn

            with patch.object(repository, "POSTGRES", False), patch.object(
                repository,
                "conectar",
                conectar_prueba
            ):
                with self.assertRaisesRegex(ValueError, "Ya existe"):
                    repository.guardar_cierre_db(
                        "2026-06-29",
                        100,
                        200,
                        300,
                        "",
                        "admin",
                        "19:00:00"
                    )
        finally:
            os.remove(path)


if __name__ == "__main__":
    unittest.main()
