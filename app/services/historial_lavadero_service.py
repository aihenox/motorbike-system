from app.repositories.historial_lavadero_repository import (

    obtener_historial_lavadero_db,

    obtener_total_lavadero_db
)


# ==========================================
# LISTAR HISTORIAL LAVADERO
# ==========================================
def listar_historial_lavadero(

    placa="",

    fecha="",

    responsable=""
):

    historial_db = obtener_historial_lavadero_db(

        placa,

        fecha,

        responsable
    )

    historial = []

    for item in historial_db:

        historial.append({

            "id": item[0],

            "placa": item[1],

            "vehiculo": item[2],

            "tipo_lavado": item[3],

            "valor": item[4],

            "responsable": item[5],

            "fecha": item[6]
        })

    return historial


# ==========================================
# TOTAL LAVADERO
# ==========================================
def obtener_total_lavadero(

    placa="",

    fecha="",

    responsable=""
):

    return obtener_total_lavadero_db(

        placa,

        fecha,

        responsable
    )