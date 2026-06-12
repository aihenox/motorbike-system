from flask import (
    Blueprint,
    render_template,
    jsonify
)

from flask_login import (
    login_required
)


from app.services.dashboard_service import (
    obtener_metricas_dashboard,
    obtener_ultimos_ingresos,
    obtener_consumos_placas,
    obtener_detalle_consumos_placa
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

    consumos = obtener_consumos_placas()

    return render_template(

        "dashboard.html",

        motos=metricas.get(
            "motos_fuera",
            0
        ),

        carros=metricas.get(
            "carros_fuera",
            0
        ),

        activos=metricas.get(
            "total_activos",
            0
        ),

        total_general_hoy=metricas.get(
            "total_general_hoy",
            0
        ),

        total=metricas.get(
            "total_activos",
            0
        ),

        dinero=metricas.get(
            "total_general_hoy",
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

        movimientos=movimientos,

        consumos=consumos
    )

# ==========================================
# DETALLE CONSUMOS PLACA
# ==========================================
@dashboard_bp.route(
    "/dashboard/consumos/<placa>"
)
@login_required
def detalle_consumos_placa(
    placa
):

    data = obtener_detalle_consumos_placa(
        placa.upper()
    )

    return jsonify(data)