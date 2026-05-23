import os

from dotenv import load_dotenv

load_dotenv()


class Config:

    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "motorbike-secret-key"
    )

    BASE_DIR = os.path.abspath(
        os.path.dirname(__file__)
    )

    # ==========================================
    # CREAR CARPETAS SI NO EXISTEN
    # ==========================================
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
    # DATABASE
    # ==========================================
    DATABASE_PATH = os.path.join(
        INSTANCE_FOLDER,
        "parqueadero.db"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAX_CONTENT_LENGTH = 16 * 1024 * 1024


class DevelopmentConfig(Config):

    DEBUG = True


class ProductionConfig(Config):

    DEBUG = False


config = {

    "development": DevelopmentConfig,

    "production": ProductionConfig,

    "default": DevelopmentConfig,
}