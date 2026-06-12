from app.repositories.dashboard_repository import (

    obtener_metricas_dashboard_db,

    obtener_ultimos_ingresos_db,

    obtener_consumos_placas_db,

    obtener_detalle_consumos_placa_db

)

# ==========================================
# MÉTRICAS DASHBOARD
# ==========================================
def obtener_metricas_dashboard():

    return obtener_metricas_dashboard_db()


# ==========================================
# ÚLTIMOS MOVIMIENTOS
# ==========================================
def obtener_ultimos_ingresos(
    limite=10
):

    return obtener_ultimos_ingresos_db(
        limite
    )

# ==========================================
# CONSUMOS POR PLACA
# ==========================================
def obtener_consumos_placas():

    return obtener_consumos_placas_db()

# ==========================================
# DETALLE CONSUMOS PLACA
# ==========================================
def obtener_detalle_consumos_placa(
    placa
):

    return obtener_detalle_consumos_placa_db(
        placa
    )

# ==========================================
# DETALLE CONSUMOS PLACA
# ==========================================
def obtener_detalle_consumos_placa(
    placa
):

    return obtener_detalle_consumos_placa_db(
        placa
    )