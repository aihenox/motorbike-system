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
    current_user,
    login_required
)

from app.security import admin_required

from datetime import datetime
from io import BytesIO
from zoneinfo import ZoneInfo

import pandas as pd

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
@admin_required
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

        ahora = datetime.now(
            ZoneInfo("America/Bogota")
        )

        fecha = ahora.strftime(
            "%Y-%m-%d"
        )

        hora_cierre = ahora.strftime(
            "%H:%M:%S"
        )

        try:

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

                current_user.usuario or current_user.id,

                hora_cierre
            )

        except ValueError as error:

            flash(
                str(error),
                "danger"
            )

            return redirect(
                url_for("cierre.cierre_caja")
            )

        flash(
            "Cierre de caja guardado correctamente.",
            "success"
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

    archivo = BytesIO()

    df.to_excel(
        archivo,
        index=False
    )

    archivo.seek(0)

    # ==========================================
    # DESCARGAR
    # ==========================================
    return send_file(

        archivo,

        as_attachment=True,

        download_name="historial_cierres.xlsx",

        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
