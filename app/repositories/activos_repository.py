from app.repositories.connection import conectar


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

        c.execute("""
        SELECT *

        FROM ingresos

        WHERE id = ?
        """, (
            id,
        ))

        return c.fetchone()


# ==========================================
# ACTUALIZAR VEHÍCULO
# ==========================================
def actualizar_vehiculo_db(id, placa, tipo):

    with conectar() as conn:

        c = conn.cursor()

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

        c.execute("""
        DELETE FROM ingresos

        WHERE id = ?
        """, (
            id,
        ))

        conn.commit()