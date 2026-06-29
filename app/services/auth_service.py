from flask import current_app

from flask_login import UserMixin

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from app.repositories.auth_repository import (
    obtener_usuario_por_username,
    obtener_usuario_por_id,
    crear_usuario
)


# ==========================================
# USUARIO FLASK-LOGIN
# ==========================================
class User(UserMixin):

    def __init__(
        self,
        user_id,
        usuario=None,
        rol=None
    ):

        self.id = str(user_id)

        self.usuario = usuario

        self.rol = rol


def cargar_usuario(user_id):

    user = obtener_usuario_por_id(
        user_id
    )

    if not user:

        return None

    return User(
        user["id"],
        user["usuario"],
        user["rol"]
    )


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

    password_admin = current_app.config.get(
        "ADMIN_PASSWORD"
    )

    if not password_admin or password_admin == "change-me":

        raise RuntimeError(
            "ADMIN_PASSWORD debe configurarse antes de crear el administrador."
        )

    password_hash = generar_hash_password(
        password_admin
    )

    crear_usuario(
        usuario_admin,
        password_hash,
        "Administrador"
    )
