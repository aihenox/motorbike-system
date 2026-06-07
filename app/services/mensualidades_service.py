from app.repositories.mensualidades_repository import (
    obtener_mensualidades_db,
    crear_mensualidad_db,
    obtener_mensualidad_db,
    actualizar_mensualidad_db,
    eliminar_mensualidad_db,
    buscar_mensualidad_activa_db
)


# ==========================================
# LISTAR MENSUALIDADES
# ==========================================
def listar_mensualidades():

    return obtener_mensualidades_db()

# ==========================================
# CREAR MENSUALIDAD
# ==========================================
def crear_mensualidad(

    placa,

    tipo,

    propietario,

    telefono,

    fecha_inicio,

    fecha_fin,

    estado
):

    crear_mensualidad_db(

        placa,

        tipo,

        propietario,

        telefono,

        fecha_inicio,

        fecha_fin,

        estado
    )

# ==========================================
# OBTENER MENSUALIDAD
# ==========================================
def obtener_mensualidad(id):

    return obtener_mensualidad_db(
        id
    )


# ==========================================
# ACTUALIZAR MENSUALIDAD
# ==========================================
def actualizar_mensualidad(

    id,

    placa,

    tipo,

    propietario,

    telefono,

    fecha_inicio,

    fecha_fin,

    estado
):

    actualizar_mensualidad_db(

        id,

        placa,

        tipo,

        propietario,

        telefono,

        fecha_inicio,

        fecha_fin,

        estado
    )

# ==========================================
# ELIMINAR MENSUALIDAD
# ==========================================
def eliminar_mensualidad(id):

    eliminar_mensualidad_db(
        id
    )

# ==========================================
# BUSCAR MENSUALIDAD ACTIVA
# ==========================================
def buscar_mensualidad_activa(
    placa
):

    return buscar_mensualidad_activa_db(
        placa
    )