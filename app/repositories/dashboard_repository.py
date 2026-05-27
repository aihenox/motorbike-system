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

        # ==========================================
        # VEHÍCULOS DENTRO
        # ==========================================
        c.execute("""

            SELECT COUNT(*)

            FROM ingresos

            WHERE estado = 'Dentro'

        """)

        total_activos = obtener_valor(
            c.fetchone()
        )

        c.execute("""

            SELECT COUNT(*)

            FROM ingresos

            WHERE estado = 'Dentro'
            AND tipo = 'Moto'

        """)

        motos_activas = obtener_valor(
            c.fetchone()
        )

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
        # TOTAL PARQUEADERO
        # ==========================================
        c.execute("""

            SELECT COALESCE(
                SUM(valor),
                0
            )

            FROM ingresos

            WHERE estado = 'Fuera'
            AND hora_salida::text LIKE %s

        """(f"{hoy}%",))

        total_parqueadero = obtener_valor(
            c.fetchone()
        )

        # ==========================================
        # LAVADOS MOTOS
        # ==========================================
        c.execute("""

            SELECT COUNT(*)

            FROM lavados

            WHERE vehiculo = 'Moto'
            AND fecha LIKE %s

        """(f"{hoy}%",))

        lavados_motos = obtener_valor(
            c.fetchone()
        )

        # ==========================================
        # LAVADOS CARROS
        # ==========================================
        c.execute("""

            SELECT COUNT(*)

            FROM lavados

            WHERE vehiculo = 'Carro'
            AND fecha LIKE %s

        """ (f"{hoy}%",))

        lavados_carros = obtener_valor(
            c.fetchone()
        )

        # ==========================================
        # TOTAL LAVADERO
        # ==========================================
        c.execute("""

            SELECT COALESCE(
                SUM(valor),
                0
            )

            FROM lavados        
            WHERE fecha LIKE %s
        """ (f"{hoy}%",))

        total_lavadero = obtener_valor(
            c.fetchone()
        )

        return {

            "total_activos": total_activos,

            "motos_activas": motos_activas,

            "carros_activos": carros_activos,

            "total_parqueadero": total_parqueadero,

            "lavados_motos": lavados_motos,

            "lavados_carros": lavados_carros,

            "total_servicios": total_lavadero
        }
    
# ==========================================
# ÚLTIMOS INGRESOS
# ==========================================
def obtener_ultimos_ingresos_db(
    limite=10
):

    with conectar() as conn:

        c = conn.cursor()

        query = f"""

            SELECT

                placa,
                tipo,
                hora_ingreso,
                hora_salida,
                estado

            FROM ingresos

            ORDER BY id DESC

            LIMIT {int(limite)}

        """

        c.execute(query)

        rows = c.fetchall()

        resultado = []

        for row in rows:

            if POSTGRES:

                resultado.append({

                    "placa": row["placa"],

                    "tipo": row["tipo"],

                    "hora_ingreso": formatear_fecha(
                        row["hora_ingreso"]
                    ),

                    "hora_salida": formatear_fecha(
                        row["hora_salida"]
                    ),

                    "estado": row["estado"]
                })

            else:

                resultado.append({

                    "placa": row[0],

                    "tipo": row[1],

                    "hora_ingreso": formatear_fecha(
                        row[2]
                    ),

                    "hora_salida": formatear_fecha(
                        row[3]
                    ),

                    "estado": row[4]
                })

        return resultado
