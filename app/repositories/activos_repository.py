import os

from app.repositories.connection import conectar


# ==========================================
# MOTOR DATABASE
# ==========================================
POSTGRES = os.getenv(
    "DATABASE_URL"
)


# ==========================================
# OBTENER ACTIVOS
# ==========================================
def obtener_activos_db():

    with conectar() as conn:

        c = conn.cursor()

        c.execute("""

            SELECT

                id,
                placa,
                tipo,
                modalidad,
                puesto_casco,
                cantidad_cascos,
                hora_ingreso

            FROM ingresos

            WHERE estado = 'Dentro'

            ORDER BY hora_ingreso DESC

                    """)

        return c.fetchall()


# ==========================================
# OBTENER VEHÍCULO
# ==========================================
def obtener_vehiculo_db(id):

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

                WHERE id = %s

            """, (
                id,
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

                WHERE id = ?

            """, (
                id,
            ))

        return c.fetchone()


# ==========================================
# ACTUALIZAR VEHÍCULO
# ==========================================
def actualizar_vehiculo_db(
    id,
    placa,
    tipo
):

    with conectar() as conn:

        c = conn.cursor()

        # ==========================================
        # POSTGRESQL
        # ==========================================
        if POSTGRES:

            c.execute("""

                UPDATE ingresos

                SET

                    placa = %s,
                    tipo = %s

                WHERE id = %s

            """, (

                placa.upper(),

                tipo,

                id
            ))

        # ==========================================
        # SQLITE
        # ==========================================
        else:

            c.execute("""

                UPDATE ingresos

                SET

                    placa = ?,
                    tipo = ?

                WHERE id = ?

            """, (

                placa.upper(),

                tipo,

                id
            ))

        conn.commit()


# ==========================================
# ELIMINAR VEHÍCULO
# ==========================================
def eliminar_vehiculo_db(id):

    with conectar() as conn:

        c = conn.cursor()

        # ==========================================
        # POSTGRESQL
        # ==========================================
        if POSTGRES:

            c.execute("""

                DELETE FROM ingresos

                WHERE id = %s

            """, (
                id,
            ))

        # ==========================================
        # SQLITE
        # ==========================================
        else:

            c.execute("""

                DELETE FROM ingresos

                WHERE id = ?

            """, (
                id,
            ))

        conn.commit()
