import os

from app.repositories.connection import conectar


# ==========================================
# MOTOR DATABASE
# ==========================================
POSTGRES = os.getenv(
    "DATABASE_URL"
)


# ==========================================
# VALIDAR PLACA ACTIVA
# ==========================================
def placa_activa_db(placa):

    with conectar() as conn:

        c = conn.cursor()

        # ==========================================
        # POSTGRESQL
        # ==========================================
        if POSTGRES:

            c.execute("""

                SELECT 1

                FROM ingresos

                WHERE placa = %s
                AND estado = 'Dentro'

            """, (
                placa.upper(),
            ))

        # ==========================================
        # SQLITE
        # ==========================================
        else:

            c.execute("""

                SELECT 1

                FROM ingresos

                WHERE placa = ?
                AND estado = 'Dentro'

            """, (
                placa.upper(),
            ))

        return c.fetchone() is not None


# ==========================================
# INSERTAR INGRESO
# ==========================================
def insertar_ingreso_db(

    placa,

    tipo,

    hora
):

    with conectar() as conn:

        c = conn.cursor()

        # ==========================================
        # POSTGRESQL
        # ==========================================
        if POSTGRES:

            c.execute("""

                INSERT INTO ingresos(

                    placa,
                    tipo,
                    hora_ingreso,
                    estado

                )

                VALUES (%s, %s, %s, %s)

                RETURNING id

            """, (

                placa.upper(),
                tipo,
                hora,
                "Dentro"
            ))

            ticket_id = c.fetchone()["id"]

        # ==========================================
        # SQLITE
        # ==========================================
        else:

            c.execute("""

                INSERT INTO ingresos(

                    placa,
                    tipo,
                    hora_ingreso,
                    estado

                )

                VALUES (?, ?, ?, ?)

            """, (

                placa.upper(),
                tipo,
                hora,
                "Dentro"
            ))

            ticket_id = c.lastrowid

        conn.commit()

        return ticket_id


# ==========================================
# OBTENER TICKET ACTIVO
# ==========================================
def obtener_ticket_activo_db(ticket):

    with conectar() as conn:

        c = conn.cursor()

        # ==========================================
        # POSTGRESQL
        # ==========================================
        if POSTGRES:

            c.execute("""

                SELECT *

                FROM ingresos

                WHERE id = %s
                AND estado = 'Dentro'

            """, (
                ticket,
            ))

        # ==========================================
        # SQLITE
        # ==========================================
        else:

            c.execute("""

                SELECT *

                FROM ingresos

                WHERE id = ?
                AND estado = 'Dentro'

            """, (
                ticket,
            ))

        return c.fetchone()


# ==========================================
# CERRAR TICKET
# ==========================================
def cerrar_ticket_db(

    ticket,

    hora_salida,

    valor
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

                    hora_salida = %s,
                    valor = %s,
                    estado = 'Fuera'

                WHERE id = %s

            """, (
                hora_salida,
                valor,
                ticket
            ))

        # ==========================================
        # SQLITE
        # ==========================================
        else:

            c.execute("""

                UPDATE ingresos

                SET

                    hora_salida = ?,
                    valor = ?,
                    estado = 'Fuera'

                WHERE id = ?

            """, (
                hora_salida,
                valor,
                ticket
            ))

        conn.commit()