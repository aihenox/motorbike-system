import os

from datetime import datetime
from zoneinfo import ZoneInfo

from app.repositories.connection import conectar


# ==========================================
# MOTOR DATABASE
# ==========================================
POSTGRES = os.getenv(
    "DATABASE_URL"
)


# ==========================================
# HELPER VALOR
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
# HELPER CIERRE
# ==========================================
def convertir_row_cierre(row):

    if POSTGRES:

        return {

            "id": row["id"],

            "fecha": row["fecha"],

            "total_parqueadero":
                row["total_parqueadero"],

            "total_lavadero":
                row["total_lavadero"],

            "total_general":
                row["total_general"],

            "observaciones":
                row["observaciones"],

            "usuario":
                row["usuario"],

            "hora_cierre":
                row["hora_cierre"]
        }

    return {

        "id": row[0],

        "fecha": row[1],

        "total_parqueadero": row[2],

        "total_lavadero": row[3],

        "total_general": row[4],

        "observaciones": row[5],

        "usuario": row[6],

        "hora_cierre": row[7]
    }


# ==========================================
# MÉTRICAS CIERRE
# ==========================================
def obtener_metricas_cierre_db():

    with conectar() as conn:

        c = conn.cursor()

        ahora = datetime.now(
            ZoneInfo("America/Bogota")
        )

        hoy_iso = ahora.strftime(
            "%Y-%m-%d"
        )

        hoy_legacy = ahora.strftime(
            "%d/%m/%Y"
        )

        # ==========================================
        # PARQUEADERO
        # ==========================================
        if POSTGRES:

            c.execute("""

                SELECT COALESCE(
                    SUM(valor),
                    0
                )

                FROM ingresos

                WHERE estado = 'Fuera'

                AND (
                    hora_salida LIKE %s
                    OR hora_salida LIKE %s
                )

            """, (
                f"{hoy_iso}%",
                f"{hoy_legacy}%"
            ))

        else:

            c.execute("""

                SELECT COALESCE(
                    SUM(valor),
                    0
                )

                FROM ingresos

                WHERE estado = 'Fuera'

                AND (
                    hora_salida LIKE ?
                    OR hora_salida LIKE ?
                )

            """, (
                f"{hoy_iso}%",
                f"{hoy_legacy}%"
            ))

        total_parqueadero = obtener_valor(
            c.fetchone()
        )

        # ==========================================
        # LAVADERO
        # ==========================================
        if POSTGRES:

            c.execute("""

                SELECT COALESCE(
                    SUM(valor),
                    0
                )

                FROM lavados

                WHERE fecha LIKE %s

            """, (f"{hoy_iso}%",))

        else:

            c.execute("""

                SELECT COALESCE(
                    SUM(valor),
                    0
                )

                FROM lavados

                WHERE fecha LIKE ?

            """, (f"{hoy_iso}%",))

        total_lavadero = obtener_valor(
            c.fetchone()
        )

        # ==========================================
        # TOTAL GENERAL
        # ==========================================
        total_general = (

            total_parqueadero
            +
            total_lavadero
        )

        return {

            "total_parqueadero":
                total_parqueadero,

            "total_lavadero":
                total_lavadero,

            "total_general":
                total_general
        }


# ==========================================
# GUARDAR CIERRE
# ==========================================
def guardar_cierre_db(

    fecha,

    total_parqueadero,

    total_lavadero,

    total_general,

    observaciones,

    usuario,

    hora_cierre
):

    with conectar() as conn:

        c = conn.cursor()

        if POSTGRES:

            c.execute("""

                INSERT INTO cierres_caja (

                    fecha,

                    total_parqueadero,

                    total_lavadero,

                    total_general,

                    observaciones,

                    usuario,

                    hora_cierre

                )

                VALUES (%s, %s, %s, %s, %s, %s, %s)

            """, (

                fecha,

                total_parqueadero,

                total_lavadero,

                total_general,

                observaciones,

                usuario,

                hora_cierre
            ))

        else:

            c.execute("""

                INSERT INTO cierres_caja (

                    fecha,

                    total_parqueadero,

                    total_lavadero,

                    total_general,

                    observaciones,

                    usuario,

                    hora_cierre

                )

                VALUES (?, ?, ?, ?, ?, ?, ?)

            """, (

                fecha,

                total_parqueadero,

                total_lavadero,

                total_general,

                observaciones,

                usuario,

                hora_cierre
            ))

        conn.commit()


# ==========================================
# HISTORIAL CIERRES
# ==========================================
def obtener_historial_cierres_db():

    with conectar() as conn:

        c = conn.cursor()

        c.execute("""

            SELECT
                id,
                fecha,
                total_parqueadero,
                total_lavadero,
                total_general,
                observaciones,
                usuario,
                hora_cierre

            FROM cierres_caja

            ORDER BY id DESC

        """)

        rows = c.fetchall()

        resultado = []

        for row in rows:

            resultado.append(
                convertir_row_cierre(row)
            )

        return resultado
