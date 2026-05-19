from flask import Blueprint
from flask import render_template
from flask import request
from flask import jsonify
from flask import url_for

from flask_login import login_required

from app.services.salida_service import procesar_salida

import os


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

        if not resultado["success"]:

            return jsonify({

                "success": False,

                "message": resultado["message"]

            })

        archivo = os.path.basename(
            resultado["pdf"]
        )

        pdf_url = url_for(
            "recibos.ver_recibo",
            archivo=archivo
        )

        return jsonify({

            "success": True,

            "pdf_url": pdf_url

        })

    except Exception as e:

        return jsonify({

            "success": False,

            "message": str(e)

        })