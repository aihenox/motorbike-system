from app.repositories.cierre_repository import (

    obtener_metricas_cierre_db,

    guardar_cierre_db
)


# ==========================================
# OBTENER MÉTRICAS
# ==========================================
def obtener_metricas_cierre():

    return obtener_metricas_cierre_db()


# ==========================================
# GUARDAR CIERRE
# ==========================================
def guardar_cierre(

    fecha,

    total_parqueadero,

    total_lavadero,

    total_general,

    observaciones,

    usuario,

    hora_cierre
):

    guardar_cierre_db(

        fecha,

        total_parqueadero,

        total_lavadero,

        total_general,

        observaciones,

        usuario,

        hora_cierre
    )

# ==========================================
# HISTORIAL CIERRES
# ==========================================
from app.repositories.cierre_repository import (
    obtener_historial_cierres_db
)


def obtener_historial_cierres():

    return obtener_historial_cierres_db()