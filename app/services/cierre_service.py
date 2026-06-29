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

    total_parqueadero = int(
        total_parqueadero
    )

    total_lavadero = int(
        total_lavadero
    )

    if total_parqueadero < 0 or total_lavadero < 0:

        raise ValueError(
            "Los totales del cierre no pueden ser negativos"
        )

    total_general = (
        total_parqueadero
        + total_lavadero
    )

    observaciones = (
        observaciones or ""
    ).strip()

    if len(observaciones) > 500:

        raise ValueError(
            "Las observaciones no pueden superar 500 caracteres"
        )

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
