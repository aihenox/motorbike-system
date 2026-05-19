from flask import (
    Blueprint,
    render_template
)

from flask_login import login_required

from app.services.dashboard_service import (
    obtener_metricas_dashboard,
    obtener_ultimos_ingresos
)


parqueadero_bp = Blueprint(
    "parqueadero",
    __name__
)


# ==========================================
# DASHBOARD PARQUEADERO
# ==========================================
@parqueadero_bp.route(
    "/dashboard/parqueadero"
)
@login_required
def dashboard_parqueadero():

    metricas = obtener_metricas_dashboard()

    movimientos = obtener_ultimos_ingresos()

    return render_template(

        "dashboard_parqueadero.html",

        motos=metricas.get(
            "motos_activas",
            0
        ),

        carros=metricas.get(
            "carros_activos",
            0
        ),

        total=metricas.get(
            "total_activos",
            0
        ),

        dinero=metricas.get(
            "total_parqueadero",
            0
        ),

        movimientos=movimientos
    )