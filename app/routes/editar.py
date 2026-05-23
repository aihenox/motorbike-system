from flask import (
    Blueprint,
    request,
    redirect,
    url_for
)

from flask_login import login_required

from app.services.parqueadero_service import editar_vehiculo


editar_bp = Blueprint("editar", __name__)


@editar_bp.route("/editar/<int:id>", methods=["POST"])
@login_required
def editar(id):

    placa = request.form["placa"]
    tipo = request.form["tipo"]

    editar_vehiculo(
        id,
        placa,
        tipo
    )

    return redirect(url_for("activos.activos"))