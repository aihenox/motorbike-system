from flask import Blueprint, render_template

from flask_login import login_required

from app.services.activos_service import listar_activos


activos_bp = Blueprint("activos", __name__)


@activos_bp.route("/activos")
@login_required
def activos():

    activos = listar_activos()

    return render_template(
        "activos.html",
        activos=activos
    )