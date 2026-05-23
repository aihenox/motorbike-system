from flask import Flask

from flask_login import LoginManager

from config import Config

from database import crear_bd

from app.services.auth_service import User

from app.errors import (
    register_error_handlers
)


# ==========================================
# LOGIN MANAGER
# ==========================================
login_manager = LoginManager()

login_manager.login_view = "auth.login"


# ==========================================
# USER LOADER
# ==========================================
@login_manager.user_loader
def load_user(user_id):

    return User(user_id)


# ==========================================
# CREAR APP
# ==========================================
def create_app():

    app = Flask(__name__)

    app.config.from_object(
        Config
    )

    # ==========================================
    # LOGIN
    # ==========================================
    login_manager.init_app(app)

    # ==========================================
    # CREAR DB
    # ==========================================
    with app.app_context():

        crear_bd()

    # ==========================================
    # IMPORTAR BLUEPRINTS
    # ==========================================
    from app.routes.auth import auth_bp

    from app.routes.dashboard import dashboard_bp

    from app.routes.ingreso import ingreso_bp

    from app.routes.salida import salida_bp

    from app.routes.activos import activos_bp

    from app.routes.editar import editar_bp

    from app.routes.eliminar import eliminar_bp

    from app.routes.historial import historial_bp

    from app.routes.lavadero import lavadero_bp

    from app.routes.parqueadero import parqueadero_bp

    from app.routes.cierre import cierre_bp

    from app.routes.recibos import recibos_bp

    # ==========================================
    # REGISTRAR BLUEPRINTS
    # ==========================================
    app.register_blueprint(auth_bp)

    app.register_blueprint(dashboard_bp)

    app.register_blueprint(ingreso_bp)

    app.register_blueprint(salida_bp)

    app.register_blueprint(activos_bp)

    app.register_blueprint(editar_bp)

    app.register_blueprint(eliminar_bp)

    app.register_blueprint(historial_bp)

    app.register_blueprint(lavadero_bp)

    app.register_blueprint(parqueadero_bp)

    app.register_blueprint(cierre_bp)

    app.register_blueprint(recibos_bp)

    # ==========================================
    # ERROR HANDLERS
    # ==========================================
    register_error_handlers(app)

    return app
