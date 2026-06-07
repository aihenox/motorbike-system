import os

from app.repositories.connection import conectar


POSTGRES = os.getenv(
    "DATABASE_URL"
)


# ==========================================
# LISTAR MENSUALIDADES
# ==========================================
def obtener_mensualidades_db():


    with conectar() as conn:

        c = conn.cursor()

        c.execute("""

            SELECT

                id,
                placa,
                tipo,
                propietario,
                telefono,
                fecha_inicio,
                fecha_fin,
                estado

            FROM mensualidades

            ORDER BY placa

        """)

        return c.fetchall()
    
# ==========================================
# CREAR MENSUALIDAD
# ==========================================
def crear_mensualidad_db(

    placa,

    tipo,

    propietario,

    telefono,

    fecha_inicio,

    fecha_fin,

    estado
):

    with conectar() as conn:

        c = conn.cursor()

        if POSTGRES:

            c.execute("""

                INSERT INTO mensualidades(

                    placa,
                    tipo,
                    propietario,
                    telefono,
                    fecha_inicio,
                    fecha_fin,
                    estado

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

            """, (

                placa.upper(),
                tipo,
                propietario,
                telefono,
                fecha_inicio,
                fecha_fin,
                estado

            ))

        else:

            c.execute("""

                INSERT INTO mensualidades(

                    placa,
                    tipo,
                    propietario,
                    telefono,
                    fecha_inicio,
                    fecha_fin,
                    estado

                )

                VALUES (?, ?, ?, ?, ?, ?, ?)

            """, (

                placa.upper(),
                tipo,
                propietario,
                telefono,
                fecha_inicio,
                fecha_fin,
                estado

            ))

        conn.commit()