from flask import (

    Blueprint,

    render_template,

    request,

    redirect,

    url_for,

    flash,

    send_file
)

from flask_login import (
    login_required
)

from datetime import datetime

import pandas as pd

import os

from app.services.cierre_service import (

    obtener_metricas_cierre,

    guardar_cierre,

    obtener_historial_cierres
)


cierre_bp = Blueprint(

    "cierre",

    __name__
)


# ==========================================
# CIERRE CAJA
# ==========================================
@cierre_bp.route(

    "/cierre-caja",

    methods=["GET", "POST"]
)
@login_required
def cierre_caja():

    metricas = obtener_metricas_cierre()

    # ==========================================
    # GUARDAR CIERRE
    # ==========================================
    if request.method == "POST":

        observaciones = request.form.get(

            "observaciones",

            ""
        )

        ahora = datetime.now()

        fecha = ahora.strftime(
            "%d/%m/%Y"
        )

        hora_cierre = ahora.strftime(
            "%H:%M:%S"
        )

        guardar_cierre(

            fecha,

            metricas[
                "total_parqueadero"
            ],

            metricas[
                "total_lavadero"
            ],

            metricas[
                "total_general"
            ],

            observaciones,

            "admin",

            hora_cierre
        )

        flash(
            "Cierre de caja guardado correctamente."
        )

        return redirect(
            url_for(
                "cierre.cierre_caja"
            )
        )

    return render_template(

        "cierre_caja.html",

        total_parqueadero=
            metricas[
                "total_parqueadero"
            ],

        total_lavadero=
            metricas[
                "total_lavadero"
            ],

        total_general=
            metricas[
                "total_general"
            ]
    )


# ==========================================
# HISTORIAL CIERRES
# ==========================================
@cierre_bp.route(
    "/historial-cierres"
)
@login_required
def historial_cierres():

    historial = obtener_historial_cierres()

    total_general = sum(

        item["total_general"]

        for item in historial
    )

    return render_template(

        "historial_cierres.html",

        historial=historial,

        total_general=total_general
    )


# ==========================================
# EXPORTAR EXCEL
# ==========================================
@cierre_bp.route(
    "/exportar-cierres-excel"
)
@login_required
def exportar_cierres_excel():

    historial = obtener_historial_cierres()

    df = pd.DataFrame(historial)

    # ==========================================
    # RENOMBRAR COLUMNAS
    # ==========================================
    df = df.rename(columns={

        "fecha":
            "Fecha",

        "total_parqueadero":
            "Parqueadero",

        "total_lavadero":
            "Lavadero",

        "total_general":
            "Total General",

        "usuario":
            "Usuario",

        "hora_cierre":
            "Hora Cierre",

        "observaciones":
            "Observaciones"
    })

    # ==========================================
    # ELIMINAR ID
    # ==========================================
    if "id" in df.columns:

        df = df.drop(
            columns=["id"]
        )

    # ==========================================
    # CREAR ARCHIVO
    # ==========================================
    nombre_archivo = (
        "historial_cierres.xlsx"
    )

    ruta_archivo = os.path.join(

        os.getcwd(),

        nombre_archivo
    )

    df.to_excel(

        ruta_archivo,

        index=False
    )

    # ==========================================
    # DESCARGAR
    # ==========================================
    return send_file(

        ruta_archivo,

        as_attachment=True
    )