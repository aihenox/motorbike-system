from app.repositories.historial_repository import (

    obtener_historial_db,

    buscar_por_placa_db,

    filtrar_por_fecha_db,

    eliminar_registro_historial_db
)

from app.utils.date_utils import (

    formatear_fecha,

    calcular_tiempo_transcurrido
)


# ==========================================
# FORMATEAR HISTORIAL
# ==========================================
def formatear_historial(
    historial
):

    resultado = []

    for item in historial:

        data = dict(item)

        ingreso_original = data["hora_ingreso"]

        salida_original = data["hora_salida"]

        data["tiempo_transcurrido"] = (
            calcular_tiempo_transcurrido(
                ingreso_original,
                salida_original
            )
        )

        data["hora_ingreso"] = formatear_fecha(
            ingreso_original
        )

        data["hora_salida"] = formatear_fecha(
            salida_original
        )

        resultado.append(data)

    return resultado


# ==========================================
# LISTAR HISTORIAL
# ==========================================
def listar_historial():

    historial = obtener_historial_db()

    return formatear_historial(
        historial
    )


# ==========================================
# BUSCAR PLACA
# ==========================================
def buscar_placa(
    placa
):

    historial = buscar_por_placa_db(
        placa
    )

    return formatear_historial(
        historial
    )


# ==========================================
# FILTRAR FECHA
# ==========================================
def filtrar_fecha(
    fecha
):

    historial = filtrar_por_fecha_db(
        fecha
    )

    return formatear_historial(
        historial
    )


# ==========================================
# ELIMINAR REGISTRO
# ==========================================
def eliminar_registro_historial(
    registro_id
):

    return eliminar_registro_historial_db(
        registro_id
    )
