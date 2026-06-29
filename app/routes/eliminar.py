from flask import (
    Blueprint,
    redirect,
    url_for
)

from flask_login import login_required

from app.services.parqueadero_service import borrar_vehiculo

from app.security import admin_required


eliminar_bp = Blueprint("eliminar", __name__)


@eliminar_bp.route(
    "/eliminar/<int:id>",
    methods=["POST"]
)
@login_required
@admin_required
def eliminar(id):

    borrar_vehiculo(id)

    return redirect(url_for("activos.activos"))
