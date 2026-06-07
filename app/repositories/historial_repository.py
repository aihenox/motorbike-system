import os

from app.repositories.connection import conectar


# ==========================================
# MOTOR DATABASE
# ==========================================
POSTGRES = os.getenv(
    "DATABASE_URL"
)


# ==========================================
# HELPER HISTORIAL
# ==========================================
def convertir_row_historial(row):

    if POSTGRES:

        return {

            "id": row["id"],

            "placa": row["placa"],

            "tipo": row["tipo"],

            "modalidad": row["modalidad"],

            "hora_ingreso": row["hora_ingreso"],

            "hora_salida": row["hora_salida"],

            "valor": row["valor"],

            "estado": row["estado"]
        }

    return {

        "id": row[0],

        "placa": row[1],

        "tipo": row[2],

        "modalidad": row[3],

        "hora_ingreso": row[4],

        "hora_salida": row[5],

        "valor": row[6],

        "estado": row[7]
    }
# ==========================================
# OBTENER HISTORIAL
# ==========================================
def obtener_historial_db():

    with conectar() as conn:

        c = conn.cursor()

        c.execute("""

            SELECT

                id,
                placa,
                tipo,
                modalidad,
                hora_ingreso,
                hora_salida,
                valor,
                estado

            FROM ingresos

            ORDER BY id DESC

        """)

        rows = c.fetchall()

        resultado = []

        for row in rows:

            resultado.append(
                convertir_row_historial(row)
            )

        return resultado


# ==========================================
# BUSCAR POR PLACA
# ==========================================
def buscar_por_placa_db(
    placa
):

    with conectar() as conn:

        c = conn.cursor()

        # ==========================================
        # POSTGRESQL
        # ==========================================
        if POSTGRES:

            c.execute("""

                SELECT

                    id,
                    placa,
                    tipo,
                    modalidad,
                    hora_ingreso,
                    hora_salida,
                    valor,
                    estado

                FROM ingresos

                WHERE placa LIKE %s

                ORDER BY id DESC

            """, (
                f"%{placa.upper()}%",
            ))

        # ==========================================
        # SQLITE
        # ==========================================
        else:

            c.execute("""

                SELECT

                    id,
                    placa,
                    tipo,
                    modalidad,
                    hora_ingreso,
                    hora_salida,
                    valor,
                    estado

                FROM ingresos

                WHERE placa LIKE ?

                ORDER BY id DESC

            """, (
                f"%{placa.upper()}%",
            ))

        rows = c.fetchall()

        resultado = []

        for row in rows:

            resultado.append(
                convertir_row_historial(row)
            )

        return resultado


# ==========================================
# FILTRAR POR FECHA
# ==========================================
def filtrar_por_fecha_db(
    fecha
):

    with conectar() as conn:

        c = conn.cursor()

        # ==========================================
        # POSTGRESQL
        # ==========================================
        if POSTGRES:

            c.execute("""

                SELECT

                    id,
                    placa,
                    tipo,
                    hora_ingreso,
                    hora_salida,
                    valor,
                    estado

                FROM ingresos

                WHERE hora_ingreso LIKE %s

                ORDER BY id DESC

            """, (
                f"%{fecha}%",
            ))

        # ==========================================
        # SQLITE
        # ==========================================
        else:

            c.execute("""

                SELECT

                    id,
                    placa,
                    tipo,
                    hora_ingreso,
                    hora_salida,
                    valor,
                    estado

                FROM ingresos

                WHERE hora_ingreso LIKE ?

                ORDER BY id DESC

            """, (
                f"%{fecha}%",
            ))

        rows = c.fetchall()

        resultado = []

        for row in rows:

            resultado.append(
                convertir_row_historial(row)
            )

        return resultado


# ==========================================
# ELIMINAR REGISTRO
# ==========================================
def eliminar_registro_historial_db(
    registro_id
):

    with conectar() as conn:

        c = conn.cursor()

        if POSTGRES:

            c.execute("""

                DELETE FROM ingresos

                WHERE id = %s
                AND estado = 'Fuera'

            """, (
                registro_id,
            ))

        else:

            c.execute("""

                DELETE FROM ingresos

                WHERE id = ?
                AND estado = 'Fuera'

            """, (
                registro_id,
            ))

        filas_eliminadas = c.rowcount

        conn.commit()

        return filas_eliminadas > 0
