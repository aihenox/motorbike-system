from flask import (
    Blueprint,
    render_template
)

from flask_login import (
    login_required
)


from app.services.dashboard_service import (
    obtener_metricas_dashboard,
    obtener_ultimos_ingresos
)


dashboard_bp = Blueprint(
    "dashboard",
    __name__
)


# ==========================================
# DASHBOARD GENERAL
# ==========================================
@dashboard_bp.route("/dashboard")
@login_required
def dashboard():

    metricas = obtener_metricas_dashboard()

    movimientos = obtener_ultimos_ingresos()

    return render_template(

        "dashboard.html",

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
            "total_servicios",
            0
        ),

        lavados_motos=metricas.get(
            "lavados_motos",
            0
        ),

        lavados_carros=metricas.get(
            "lavados_carros",
            0
        ),

        movimientos=movimientos
    )