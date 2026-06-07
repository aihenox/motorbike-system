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

        if POSTGRES:

            c.execute("""

                SELECT 1

                FROM ingresos

                WHERE placa = %s
                AND estado = 'Dentro'

            """, (
                placa.upper(),
            ))

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
# VALIDAR PUESTO CASCO
# ==========================================
def puesto_casco_ocupado_db(
    puesto
):

    if not puesto:

        return False

    with conectar() as conn:

        c = conn.cursor()

        if POSTGRES:

            c.execute("""

                SELECT 1

                FROM ingresos

                WHERE estado = 'Dentro'
                AND puesto_casco = %s

            """, (
                puesto,
            ))

        else:

            c.execute("""

                SELECT 1

                FROM ingresos

                WHERE estado = 'Dentro'
                AND puesto_casco = ?

            """, (
                puesto,
            ))

        return c.fetchone() is not None


# ==========================================
# INSERTAR INGRESO
# ==========================================
def insertar_ingreso_db(

    placa,

    tipo,

    hora,

    modalidad="Hora",

    puesto_casco=None,

    cantidad_cascos=0
):

    with conectar() as conn:

        c = conn.cursor()

        if POSTGRES:

            c.execute("""

                INSERT INTO ingresos(

                    placa,
                    tipo,
                    hora_ingreso,
                    estado,
                    modalidad,
                    puesto_casco,
                    cantidad_cascos

                )

                VALUES (
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s
                )

                RETURNING id

            """, (

                placa.upper(),
                tipo,
                hora,
                "Dentro",
                modalidad,
                puesto_casco,
                cantidad_cascos
            ))

            ticket_id = c.fetchone()["id"]

        else:

            c.execute("""

                INSERT INTO ingresos(

                    placa,
                    tipo,
                    hora_ingreso,
                    estado,
                    modalidad,
                    puesto_casco,
                    cantidad_cascos

                )

                VALUES (?, ?, ?, ?, ?, ?, ?)

            """, (

                placa.upper(),
                tipo,
                hora,
                "Dentro",
                modalidad,
                puesto_casco,
                cantidad_cascos
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

        if POSTGRES:

            c.execute("""

                SELECT
                    id,
                    placa,
                    tipo,
                    modalidad,
                    puesto_casco,
                    cantidad_cascos,
                    hora_ingreso,
                    hora_salida,
                    valor,
                    estado

                FROM ingresos

                WHERE id = %s
                AND estado = 'Dentro'

            """, (
                ticket,
            ))

        else:

            c.execute("""

                SELECT
                    id,
                    placa,
                    tipo,
                    modalidad,
                    puesto_casco,
                    cantidad_cascos,
                    hora_ingreso,
                    hora_salida,
                    valor,
                    estado

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