import os

from app.repositories.connection import (
    conectar
)


# ==========================================
# MOTOR DATABASE
# ==========================================
POSTGRES = os.getenv(
    "DATABASE_URL"
)


# ==========================================
# OBTENER USUARIO USERNAME
# ==========================================
def obtener_usuario_por_username(
    usuario
):

    with conectar() as conn:

        c = conn.cursor()

        # ==========================================
        # POSTGRESQL
        # ==========================================
        if POSTGRES:

            c.execute("""

                SELECT *

                FROM usuarios

                WHERE usuario = %s

            """, (usuario,))

            return c.fetchone()

        # ==========================================
        # SQLITE
        # ==========================================
        else:

            c.execute("""

                SELECT *

                FROM usuarios

                WHERE usuario = ?

            """, (usuario,))

            return c.fetchone()


# ==========================================
# OBTENER USUARIO ID
# ==========================================
def obtener_usuario_por_id(
    user_id
):

    with conectar() as conn:

        c = conn.cursor()

        # ==========================================
        # POSTGRESQL
        # ==========================================
        if POSTGRES:

            c.execute("""

                SELECT *

                FROM usuarios

                WHERE id = %s

            """, (user_id,))

            return c.fetchone()

        # ==========================================
        # SQLITE
        # ==========================================
        else:

            c.execute("""

                SELECT *

                FROM usuarios

                WHERE id = ?

            """, (user_id,))

            return c.fetchone()


# ==========================================
# CREAR USUARIO
# ==========================================
def crear_usuario(

    usuario,

    password,

    rol
):

    with conectar() as conn:

        c = conn.cursor()

        # ==========================================
        # POSTGRESQL
        # ==========================================
        if POSTGRES:

            c.execute("""

                INSERT INTO usuarios (

                    usuario,

                    password,

                    rol

                )

                VALUES (%s, %s, %s)

            """, (

                usuario,

                password,

                rol
            ))

        # ==========================================
        # SQLITE
        # ==========================================
        else:

            c.execute("""

                INSERT INTO usuarios (

                    usuario,

                    password,

                    rol

                )

                VALUES (?, ?, ?)

            """, (

                usuario,

                password,

                rol
            ))

        conn.commit()