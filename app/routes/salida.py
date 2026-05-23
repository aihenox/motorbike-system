from flask import (
    Blueprint,
    render_template,
    request,
    jsonify
)

from flask_login import login_required

from app.services.salida_service import (
    procesar_salida
)


salida_bp = Blueprint(
    "salida",
    __name__
)


# ==========================================
# VISTA SALIDA
# ==========================================
@salida_bp.route(
    "/salida",
    methods=["GET"]
)
@login_required
def salida():

    return render_template(
        "salida.html"
    )


# ==========================================
# PROCESAR SALIDA AJAX
# ==========================================
@salida_bp.route(
    "/procesar_salida",
    methods=["POST"]
)
@login_required
def procesar_salida_ajax():

    try:

        ticket = request.form["ticket"]

        resultado = procesar_salida(
            ticket
        )

        return jsonify(
            resultado
        )

    except Exception as e:

        return jsonify({

            "success": False,

            "message": str(e)

        })