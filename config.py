import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    """
    Configuración base del sistema
    """

    # ==========================================
    # SEGURIDAD
    # ==========================================

    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "motorbike-secret-key"
    )

    # ==========================================
    # RUTAS DEL PROYECTO
    # ==========================================

    BASE_DIR = os.path.abspath(
        os.path.dirname(__file__)
    )

    INSTANCE_FOLDER = os.path.join(
        BASE_DIR,
        "instance"
    )

    RECIBOS_FOLDER = os.path.join(
        BASE_DIR,
        "recibos"
    )

    os.makedirs(
        INSTANCE_FOLDER,
        exist_ok=True
    )

    os.makedirs(
        RECIBOS_FOLDER,
        exist_ok=True
    )

    # ==========================================
    # BASE DE DATOS
    # ==========================================

    DATABASE_PATH = os.path.join(
        INSTANCE_FOLDER,
        "parqueadero.db"
    )

    DATABASE_URL = os.getenv(
        "DATABASE_URL"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # ==========================================
    # ARCHIVOS
    # ==========================================

    MAX_CONTENT_LENGTH = (
        16 * 1024 * 1024
    )

    # ==========================================
    # CONFIGURACIÓN GENERAL
    # ==========================================

    TIMEZONE = "America/Bogota"

    ADMIN_PASSWORD = os.getenv(
        "ADMIN_PASSWORD",
        "change-me"
    )


class DevelopmentConfig(Config):

    DEBUG = True


class ProductionConfig(Config):

    DEBUG = False


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}