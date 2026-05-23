from flask import (
    Blueprint,
    render_template,
    request,
    jsonify
)

from flask_login import login_required

from app.services.parqueadero_service import (
    registrar_ingreso
)


ingreso_bp = Blueprint(
    "ingreso",
    __name__
)


# ==========================================
# VISTA INGRESO
# ==========================================
@ingreso_bp.route(
    "/ingreso",
    methods=["GET"]
)
@login_required
def ingreso():

    return render_template(
        "ingreso.html"
    )


# ==========================================
# REGISTRAR INGRESO AJAX
# ==========================================
@ingreso_bp.route(
    "/registrar_ingreso",
    methods=["POST"]
)
@login_required
def registrar_ingreso_ajax():

    placa = request.form["placa"]

    tipo = request.form["tipo"]

    resultado = registrar_ingreso(
        placa,
        tipo
    )

    return jsonify(
        resultado
    )