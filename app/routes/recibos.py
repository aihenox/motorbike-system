from flask import (
    Blueprint,
    send_from_directory
)

from config import Config


recibos_bp = Blueprint("recibos", __name__)


@recibos_bp.route("/ver_recibo/<archivo>")
def ver_recibo(archivo):

    return send_from_directory(
        Config.RECIBOS_FOLDER,
        archivo
    )