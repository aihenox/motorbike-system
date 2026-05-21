from app.repositories.lavadero_repository import (

    registrar_lavado_db,

    obtener_lavados_db,

    obtener_historial_lavados_db,

    obtener_metricas_lavadero_db,

    obtener_ultimos_lavados_db,

    obtener_estadisticas_responsables_db,

    obtener_lavado_por_id_db,

    actualizar_lavado_db
)


# ==========================================
# REGISTRAR LAVADO
# ==========================================
def registrar_lavado(

    placa,

    vehiculo,

    tipo_lavado,

    valor,

    responsable,

    fecha
):

    registrar_lavado_db(

        placa,

        vehiculo,

        tipo_lavado,

        valor,

        responsable,

        fecha
    )


# ==========================================
# LISTAR LAVADOS
# ==========================================
def listar_lavados():

    return obtener_ultimos_lavados_db()


# ==========================================
# HISTORIAL LAVADOS
# ==========================================
def obtener_historial_lavados(

    placa="",

    fecha="",

    responsable=""
):

    return obtener_historial_lavados_db(

        placa,

        fecha,

        responsable
    )


# ==========================================
# METRICAS LAVADERO
# ==========================================
def obtener_metricas_lavadero():

    return obtener_metricas_lavadero_db()


# ==========================================
# ULTIMOS LAVADOS
# ==========================================
def obtener_ultimos_lavados():

    return obtener_ultimos_lavados_db()


# ==========================================
# ESTADISTICAS RESPONSABLES
# ==========================================
def obtener_estadisticas_responsables():

    return obtener_estadisticas_responsables_db()


# ==========================================
# OBTENER LAVADO POR ID
# ==========================================
def obtener_lavado_por_id(

    lavado_id
):

    return obtener_lavado_por_id_db(
        lavado_id
    )


# ==========================================
# ACTUALIZAR LAVADO
# ==========================================
def actualizar_lavado(

    lavado_id,

    placa,

    vehiculo,

    tipo_lavado,

    valor,

    responsable
):

    actualizar_lavado_db(

        lavado_id,

        placa,

        vehiculo,

        tipo_lavado,

        valor,

        responsable
    )