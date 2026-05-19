from app.repositories.dashboard_repository import (
    obtener_metricas_dashboard_db,
    obtener_ultimos_ingresos_db
)


# ==========================================
# MÉTRICAS DASHBOARD
# ==========================================
def obtener_metricas_dashboard():

    return obtener_metricas_dashboard_db()


# ==========================================
# ÚLTIMOS MOVIMIENTOS
# ==========================================
def obtener_ultimos_ingresos():

    return obtener_ultimos_ingresos_db()