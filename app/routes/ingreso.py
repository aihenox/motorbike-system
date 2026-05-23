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

from app.utils.validators import (
    validar_placa,
    validar_tipo_vehiculo
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

    try:

        placa = validar_placa(
            request.form.get("placa")
        )

        tipo = validar_tipo_vehiculo(
            request.form.get("tipo")
        )

        resultado = registrar_ingreso(
            placa,
            tipo
        )

        return jsonify(resultado)

    except ValueError as e:

        return jsonify({
            "success": False,
            "message": str(e)
        }), 400
    
    except Exception as e:

        return jsonify({
            "success": False,
            "message": "Error interno del sistema"
        }), 500