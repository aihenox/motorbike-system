from app.repositories.mensualidades_repository import (
    obtener_mensualidades_db,
    crear_mensualidad_db
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