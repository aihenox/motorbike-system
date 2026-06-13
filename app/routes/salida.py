from flask import (
    Blueprint,
    render_template,
    request,
    jsonify
)

from flask_login import login_required

from app.services.salida_service import (
    procesar_salida,
    confirmar_salida
)

from app.utils.validators import (
    validar_id
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

        ticket = validar_id(
            request.form.get("ticket")
        )

        resultado = procesar_salida(
            ticket
        )

        return jsonify(
            resultado
        )

    except ValueError as e:

        return jsonify({

            "success": False,

            "message": str(e)

        }), 400

    except Exception:

        return jsonify({

            "success": False,

            "message": "Error interno del sistema"

        }), 500

# ==========================================
# CONFIRMAR SALIDA AJAX
# ==========================================
@salida_bp.route(
    "/confirmar_salida",
    methods=["POST"]
)
@login_required
def confirmar_salida_ajax():

    try:

        ticket = validar_id(
            request.form.get(
                "ticket"
            )
        )

        valor = int(
            request.form.get(
                "valor"
            )
        )

        hora_salida = request.form.get(
            "hora_salida"
        )

        resultado = confirmar_salida(

            ticket,

            valor,

            hora_salida

        )

        return jsonify(
            resultado
        )

    except ValueError as e:

        return jsonify({

            "success": False,

            "message": str(e)

        }), 400

    except Exception as e:

        return jsonify({

            "success": False,

            "message": str(e)

        }), 500