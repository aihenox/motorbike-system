import os

from flask_login import UserMixin

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from app.repositories.auth_repository import (
    obtener_usuario_por_username,
    crear_usuario
)


# ==========================================
# USUARIO FLASK-LOGIN
# ==========================================
class User(UserMixin):

    def __init__(self, user_id):

        self.id = str(user_id)


# ==========================================
# VALIDAR LOGIN
# ==========================================
def validar_login(
    usuario,
    password
):

    user = obtener_usuario_por_username(
        usuario
    )

    if not user:

        return None

    if not check_password_hash(
        user["password"],
        password
    ):

        return None

    return user


# ==========================================
# GENERAR HASH
# ==========================================
def generar_hash_password(
    password
):

    return generate_password_hash(
        password
    )


# ==========================================
# CREAR ADMINISTRADOR
# ==========================================
def crear_admin_default():

    usuario_admin = "admin"

    existe = obtener_usuario_por_username(
        usuario_admin
    )

    if existe:

        return

    password_admin = os.getenv(
        "ADMIN_PASSWORD",
        "7823"
    )

    password_hash = generar_hash_password(
        password_admin
    )

    crear_usuario(
        usuario_admin,
        password_hash,
        "Administrador"
    )