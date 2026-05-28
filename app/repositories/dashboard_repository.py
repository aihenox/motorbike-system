import os

from app.repositories.connection import conectar

from app.utils.date_utils import formatear_fecha

from datetime import datetime

from zoneinfo import ZoneInfo


# ==========================================
# MOTOR DATABASE
# ==========================================
POSTGRES = os.getenv(
    "DATABASE_URL"
)


# ==========================================
# HELPER FETCH
# ==========================================
def obtener_valor(row):

    if not row:
        return 0

    if POSTGRES:
        return list(row.values())[0] or 0

    return row[0] or 0


# ==========================================
# MÉTRICAS DASHBOARD
# ==========================================
def obtener_metricas_dashboard_db():

    with conectar() as conn:

        c = conn.cursor()

        hoy = datetime.now(
            ZoneInfo("America/Bogota")
        ).strftime("%Y-%m-%d")

        operador = "%s" if POSTGRES else "?"

        # ==========================================
        # VEHÍCULOS ACTIVOS
        # ==========================================
        c.execute("""

            SELECT COUNT(*)

            FROM ingresos

            WHERE estado = 'Dentro'

        """)

        total_activos = obtener_valor(
            c.fetchone()
        )

        # ==========================================
        # MOTOS FUERA HOY
        # ==========================================
        c.execute(f"""

            SELECT COUNT(*)

            FROM ingresos

            WHERE estado = 'Fuera'
            AND tipo = 'Moto'
            AND hora_salida LIKE {operador}

        """, (
            f"{hoy}%",
        ))

        motos_fuera = obtener_valor(
            c.fetchone()
        )

        # ==========================================
        # CARROS FUERA HOY
        # ==========================================
        c.execute(f"""

            SELECT COUNT(*)

            FROM ingresos

            WHERE estado = 'Fuera'
            AND tipo = 'Carro'
            AND hora_salida LIKE {operador}

        """, (
            f"{hoy}%",
        ))

        carros_fuera = obtener_valor(
            c.fetchone()
        )

        # ==========================================
        # TOTAL PARQUEADERO HOY
        # ==========================================
        c.execute(f"""

            SELECT COALESCE(
                SUM(valor),
                0
            )

            FROM ingresos

            WHERE estado = 'Fuera'
            AND hora_salida LIKE {operador}

        """, (
            f"{hoy}%",
        ))

        total_parqueadero = obtener_valor(
            c.fetchone()
        )

        # ==========================================
        # LAVADOS MOTOS HOY
        # ==========================================
        c.execute(f"""

            SELECT COUNT(*)

            FROM lavados

            WHERE vehiculo = 'Moto'
            AND fecha LIKE {operador}

        """, (
            f"{hoy}%",
        ))

        lavados_motos = obtener_valor(
            c.fetchone()
        )

        # ==========================================
        # LAVADOS CARROS HOY
        # ==========================================
        c.execute(f"""

            SELECT COUNT(*)

            FROM lavados

            WHERE vehiculo = 'Carro'
            AND fecha LIKE {operador}

        """, (
            f"{hoy}%",
        ))

        lavados_carros = obtener_valor(
            c.fetchone()
        )

        # ==========================================
        # TOTAL LAVADERO HOY
        # ==========================================
        c.execute(f"""

            SELECT COALESCE(
                SUM(valor),
                0
            )

            FROM lavados

            WHERE fecha LIKE {operador}

        """, (
            f"{hoy}%",
        ))

        total_lavadero = obtener_valor(
            c.fetchone()
        )

        # ==========================================
        # TOTAL GENERAL HOY
        # ==========================================
        total_general_hoy = (
            total_parqueadero +
            total_lavadero
        )

        return {

            "total_activos": total_activos,

            "motos_fuera": motos_fuera,

            "carros_fuera": carros_fuera,

            "total_parqueadero": total_parqueadero,

            "lavados_motos": lavados_motos,

            "lavados_carros": lavados_carros,

            "total_servicios": total_lavadero,

            "total_general_hoy": total_general_hoy
        }