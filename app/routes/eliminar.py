from flask import (
    Blueprint,
    redirect,
    url_for
)

from flask_login import login_required

from app.services.parqueadero_service import borrar_vehiculo


eliminar_bp = Blueprint("eliminar", __name__)


@eliminar_bp.route("/eliminar/<int:id>")
@login_required
def eliminar(id):

    borrar_vehiculo(id)

    return redirect(url_for("activos.activos"))