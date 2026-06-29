import os
import re
import sqlite3
import tempfile
import unittest
from contextlib import closing, contextmanager
from unittest.mock import patch


class CafeteriaServiceTests(unittest.TestCase):

    def test_rechaza_cantidad_negativa(self):
        from app.services.cafeteria_service import registrar_venta_cafeteria

        with self.assertRaisesRegex(ValueError, "mayor que cero"):
            registrar_venta_cafeteria(
                [{"producto_id": 1, "cantidad": -2}],
                "ABC123",
                "1",
                "2026-06-28 10:00:00"
            )


class CafeteriaRepositoryTests(unittest.TestCase):

    def setUp(self):
        handle, self.path = tempfile.mkstemp(suffix=".db")
        os.close(handle)

        with closing(sqlite3.connect(self.path)) as conn:
            conn.executescript("""
                CREATE TABLE productos_cafeteria(
                    id INTEGER PRIMARY KEY,
                    nombre TEXT,
                    precio INTEGER,
                    inventario INTEGER
                );
                CREATE TABLE ventas_cafeteria(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    venta_id TEXT,
                    fecha TEXT,
                    producto_id INTEGER,
                    producto TEXT,
                    cantidad INTEGER,
                    valor_unitario INTEGER,
                    total INTEGER,
                    placa TEXT,
                    usuario TEXT
                );
                INSERT INTO productos_cafeteria
                    (id, nombre, precio, inventario)
                VALUES (1, 'Agua', 2000, 5);
            """)
            conn.commit()

    def tearDown(self):
        os.remove(self.path)

    @contextmanager
    def conectar(self):
        with closing(sqlite3.connect(self.path)) as conn:
            with conn:
                yield conn

    def test_venta_completa_actualiza_stock(self):
        import app.repositories.cafeteria_repository as repository

        detalles = [{
            "producto_id": 1,
            "producto": "Agua",
            "cantidad": 2,
            "valor_unitario": 2000,
            "total": 4000
        }]

        with patch.object(repository, "POSTGRES", False), \
             patch.object(repository, "conectar", self.conectar):
            repository.registrar_venta_cafeteria_lote_db(
                "venta-1",
                "2026-06-28 10:00:00",
                detalles,
                "ABC123",
                "1"
            )

        with closing(sqlite3.connect(self.path)) as conn:
            inventario = conn.execute(
                "SELECT inventario FROM productos_cafeteria WHERE id = 1"
            ).fetchone()[0]
            ventas = conn.execute(
                "SELECT COUNT(*) FROM ventas_cafeteria"
            ).fetchone()[0]

        self.assertEqual(inventario, 3)
        self.assertEqual(ventas, 1)

    def test_error_revierte_toda_la_venta(self):
        import app.repositories.cafeteria_repository as repository

        detalles = [
            {
                "producto_id": 1,
                "producto": "Agua",
                "cantidad": 2,
                "valor_unitario": 2000,
                "total": 4000
            },
            {
                "producto_id": 999,
                "producto": "Inexistente",
                "cantidad": 1,
                "valor_unitario": 1000,
                "total": 1000
            }
        ]

        with patch.object(repository, "POSTGRES", False), \
             patch.object(repository, "conectar", self.conectar):
            with self.assertRaisesRegex(ValueError, "Inventario insuficiente"):
                repository.registrar_venta_cafeteria_lote_db(
                    "venta-2",
                    "2026-06-28 10:00:00",
                    detalles,
                    "ABC123",
                    "1"
                )

        with closing(sqlite3.connect(self.path)) as conn:
            inventario = conn.execute(
                "SELECT inventario FROM productos_cafeteria WHERE id = 1"
            ).fetchone()[0]
            ventas = conn.execute(
                "SELECT COUNT(*) FROM ventas_cafeteria"
            ).fetchone()[0]

        self.assertEqual(inventario, 5)
        self.assertEqual(ventas, 0)


class SalidaTests(unittest.TestCase):

    def test_confirmacion_usa_calculo_del_servidor(self):
        import app.services.salida_service as service

        salida = {
            "success": True,
            "valor": 4500,
            "hora_salida": "28/06/2026 10:00 AM",
            "hora_salida_iso": "2026-06-28T10:00:00-05:00"
        }

        with patch.object(service, "procesar_salida", return_value=salida), \
             patch.object(service, "cerrar_ticket_db", return_value=True) as cerrar:
            resultado = service.confirmar_salida(7)

        cerrar.assert_called_once_with(
            7,
            "2026-06-28T10:00:00-05:00",
            4500
        )
        self.assertEqual(resultado["valor"], 4500)


class RutasTests(unittest.TestCase):

    def test_eliminaciones_solo_aceptan_post_y_recibos_exigen_login(self):
        import app

        with patch.object(app, "crear_bd"):
            flask_app = app.create_app()

        reglas = {rule.rule: rule for rule in flask_app.url_map.iter_rules()}

        self.assertNotIn("GET", reglas["/eliminar/<int:id>"].methods)
        self.assertNotIn(
            "GET",
            reglas["/mensualidades/eliminar/<int:id>"].methods
        )
        self.assertNotIn("GET", reglas["/logout"].methods)

        response = flask_app.test_client().get("/ver_recibo/no-existe.pdf")
        self.assertEqual(response.status_code, 302)
        self.assertIn("/", response.headers["Location"])

    def test_csrf_bloquea_post_sin_token(self):
        import app

        with patch.object(app, "crear_bd"):
            flask_app = app.create_app()

        client = flask_app.test_client()
        response = client.get("/")
        html = response.get_data(as_text=True)
        token = re.search(
            r'<meta name="csrf-token" content="([^"]+)"',
            html
        ).group(1)

        bloqueada = client.post(
            "/",
            data={"usuario": "admin", "password": "incorrecta"}
        )
        self.assertEqual(bloqueada.status_code, 400)
        self.assertIn("sesión vencida", bloqueada.get_json()["message"])

        with patch("app.routes.auth.validar_login", return_value=None):
            permitida = client.post(
                "/",
                data={"usuario": "admin", "password": "incorrecta"},
                headers={"X-CSRF-Token": token}
            )

        self.assertEqual(permitida.status_code, 200)

    def test_usuario_no_administrador_recibe_403(self):
        import app
        from app.services.auth_service import User

        with patch.object(app, "crear_bd"):
            flask_app = app.create_app()

        client = flask_app.test_client()

        with client.session_transaction() as session:
            session["_user_id"] = "2"
            session["_fresh"] = True
            session["_csrf_token"] = "token-prueba"

        operador = User(2, "operador", "Operador")

        with patch.object(app, "cargar_usuario", return_value=operador):
            response = client.post(
                "/eliminar/1",
                headers={"X-CSRF-Token": "token-prueba"}
            )

        self.assertEqual(response.status_code, 403)
        self.assertIn("Acceso denegado", response.get_data(as_text=True))


if __name__ == "__main__":
    unittest.main()
