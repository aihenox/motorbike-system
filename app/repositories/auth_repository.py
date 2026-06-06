import os

from app.repositories.connection import (
    conectar
)


# ==========================================
# PLACEHOLDER SQL
# ==========================================
def get_placeholder():

    return (
        "%s"
        if os.getenv("DATABASE_URL")
        else "?"
    )


# ==========================================
# OBTENER USUARIO USERNAME
# ==========================================
def obtener_usuario_por_username(
    usuario
):

    placeholder = get_placeholder()

    with conectar() as conn:

        c = conn.cursor()

        c.execute(f"""

            SELECT
                id,
                usuario,
                password,
                rol

            FROM usuarios

            WHERE usuario = {placeholder}

        """, (usuario,))

        return c.fetchone()


# ==========================================
# OBTENER USUARIO ID
# ==========================================
def obtener_usuario_por_id(
    user_id
):

    placeholder = get_placeholder()

    with conectar() as conn:

        c = conn.cursor()

        c.execute(f"""

            SELECT
                id,
                usuario,
                password,
                rol

            FROM usuarios

            WHERE id = {placeholder}

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

    p = get_placeholder()

    with conectar() as conn:

        c = conn.cursor()

        c.execute(f"""

            INSERT INTO usuarios (

                usuario,

                password,

                rol

            )

            VALUES (
                {p},
                {p},
                {p}
            )

        """, (

            usuario,

            password,

            rol
        ))

        conn.commit()