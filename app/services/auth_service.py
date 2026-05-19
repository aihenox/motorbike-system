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
# USER LOGIN
# ==========================================
class User(UserMixin):

    def __init__(self, user_id):

        self.id = user_id


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

    password_hash = user["password"]

    if not check_password_hash(

        password_hash,

        password
    ):

        return None

    return user


# ==========================================
# CREAR ADMIN DEFAULT
# ==========================================
def crear_admin_default():

    existe = obtener_usuario_por_username(
        "admin"
    )

    if existe:

        return

    password_hash = generate_password_hash(
        "7823"
    )

    crear_usuario(

        "admin",

        password_hash,

        "Administrador"
    )