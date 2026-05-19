import os

from datetime import datetime

from app.repositories.connection import conectar


# ==========================================
# MOTOR DATABASE
# ==========================================
POSTGRES = os.getenv(
    "DATABASE_URL"
)


# ==========================================
# FECHA HOY
# ==========================================
hoy = datetime.now().strftime(
    "%d/%m/%Y"
)


# ==========================================
# HELPER FETCH
# ==========================================
def obtener_valor(row):

    if not row:
        return 0

    # PostgreSQL
    if POSTGRES:
        return list(row.values())[0] or 0

    # SQLite
    return row[0] or 0


# ==========================================
# MÉTRICAS DASHBOARD
# ==========================================
def obtener_metricas_dashboard_db():

    with conectar() as conn:

        c = conn.cursor()

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
        # MOTOS ACTIVAS
        # ==========================================
        c.execute("""

            SELECT COUNT(*)

            FROM ingresos

            WHERE estado = 'Dentro'
            AND tipo = 'Moto'

        """)

        motos_activas = obtener_valor(
            c.fetchone()
        )

        # ==========================================
        # CARROS ACTIVOS
        # ==========================================
        c.execute("""

            SELECT COUNT(*)

            FROM ingresos

            WHERE estado = 'Dentro'
            AND tipo = 'Carro'

        """)

        carros_activos = obtener_valor(
            c.fetchone()
        )

        # ==========================================
        # LAVADOS MOTOS
        # ==========================================
        if POSTGRES:

            c.execute("""

                SELECT COUNT(*)

                FROM lavados

                WHERE vehiculo = 'Moto'

                AND fecha LIKE %s

            """, (f"{hoy}%",))

        else:

            c.execute("""

                SELECT COUNT(*)

                FROM lavados

                WHERE vehiculo = 'Moto'

                AND fecha LIKE ?

            """, (f"{hoy}%",))

        lavados_motos = obtener_valor(
            c.fetchone()
        )

        # ==========================================
        # LAVADOS CARROS
        # ==========================================
        if POSTGRES:

            c.execute("""

                SELECT COUNT(*)

                FROM lavados

                WHERE vehiculo = 'Carro'

                AND fecha LIKE %s

            """, (f"{hoy}%",))

        else:

            c.execute("""

                SELECT COUNT(*)

                FROM lavados

                WHERE vehiculo = 'Carro'

                AND fecha LIKE ?

            """, (f"{hoy}%",))

        lavados_carros = obtener_valor(
            c.fetchone()
        )

        # ==========================================
        # TOTAL PARQUEADERO
        # ==========================================
        if POSTGRES:

            c.execute("""

                SELECT COALESCE(
                    SUM(valor),
                    0
                )

                FROM ingresos

                WHERE estado = 'Fuera'

                AND hora_salida LIKE %s

            """, (f"{hoy}%",))

        else:

            c.execute("""

                SELECT COALESCE(
                    SUM(valor),
                    0
                )

                FROM ingresos

                WHERE estado = 'Fuera'

                AND hora_salida LIKE ?

            """, (f"{hoy}%",))

        total_parqueadero = obtener_valor(
            c.fetchone()
        )

        # ==========================================
        # TOTAL LAVADERO
        # ==========================================
        if POSTGRES:

            c.execute("""

                SELECT COALESCE(
                    SUM(valor),
                    0
                )

                FROM lavados

                WHERE fecha LIKE %s

            """, (f"{hoy}%",))

        else:

            c.execute("""

                SELECT COALESCE(
                    SUM(valor),
                    0
                )

                FROM lavados

                WHERE fecha LIKE ?

            """, (f"{hoy}%",))

        total_lavadero = obtener_valor(
            c.fetchone()
        )

        # ==========================================
        # TOTAL GENERAL
        # ==========================================
        total_servicios = (

            total_parqueadero
            +
            total_lavadero
        )

        return {

            "total_activos": total_activos,

            "motos_activas": motos_activas,

            "carros_activos": carros_activos,

            "lavados_motos": lavados_motos,

            "lavados_carros": lavados_carros,

            "total_parqueadero": total_parqueadero,

            "total_lavadero": total_lavadero,

            "total_servicios": total_servicios
        }


# ==========================================
# ÚLTIMOS INGRESOS
# ==========================================
def obtener_ultimos_ingresos_db():

    with conectar() as conn:

        c = conn.cursor()

        c.execute("""

            SELECT

                placa,
                tipo,
                hora_ingreso,
                estado

            FROM ingresos

            ORDER BY id DESC

            LIMIT 10

        """)

        rows = c.fetchall()

        resultado = []

        for row in rows:

            # PostgreSQL
            if POSTGRES:

                resultado.append({

                    "placa": row["placa"],

                    "tipo": row["tipo"],

                    "hora_ingreso": row["hora_ingreso"],

                    "estado": row["estado"]
                })

            # SQLite
            else:

                resultado.append({

                    "placa": row[0],

                    "tipo": row[1],

                    "hora_ingreso": row[2],

                    "estado": row[3]
                })

        return resultado