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
# FORMATEAR FECHA
# ==========================================
def formatear_fecha(fecha):

    if not fecha:
        return "-"

    try:

        dt = datetime.fromisoformat(
            fecha
        )

        return dt.strftime(
            "%d/%m/%Y %H:%M"
        )

    except:

        try:

            dt = datetime.strptime(
                fecha,
                "%d/%m/%Y %H:%M:%S"
            )

            return dt.strftime(
                "%d/%m/%Y %H:%M"
            )

        except:

            return fecha


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

        if POSTGRES:

            c.execute("""

                SELECT COALESCE(
                    SUM(valor),
                    0
                )

                FROM ingresos

                WHERE estado = 'Fuera'

            """)

        else:

            c.execute("""

                SELECT COALESCE(
                    SUM(valor),
                    0
                )

                FROM ingresos

                WHERE estado = 'Fuera'

            """)

        total_parqueadero = obtener_valor(
            c.fetchone()
        )

        return {

            "total_activos": total_activos,

            "motos_activas": motos_activas,

            "carros_activos": carros_activos,

            "total_parqueadero": total_parqueadero
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