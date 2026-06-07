from app.repositories.mensualidades_repository import (
    obtener_mensualidades_db,
    crear_mensualidad_db,
    obtener_mensualidad_db,
    actualizar_mensualidad_db,
    eliminar_mensualidad_db,
    buscar_mensualidad_activa_db
)

from datetime import date, datetime


# ==========================================
# LISTAR MENSUALIDADES
# ==========================================
def listar_mensualidades():

    registros = obtener_mensualidades_db()

    hoy = date.today()

    resultado = []

    for item in registros:

        data = dict(item)

        try:

            # ==========================
            # ESTADO INACTIVO
            # ==========================
            if data["estado"] != "Activa":

                data["vigencia"] = "Inactiva"

            else:

                fecha_fin = datetime.strptime(

                    data["fecha_fin"],

                    "%Y-%m-%d"

                ).date()

                dias = (

                    fecha_fin - hoy

                ).days

                # ==========================
                # VIGENCIA
                # ==========================
                if dias < 0:

                    data["vigencia"] = "Vencida"

                elif dias <= 3:

                    data["vigencia"] = (
                        "Próxima a vencer"
                    )

                else:

                    data["vigencia"] = "Vigente"

        except Exception:

            data["vigencia"] = (
                "Sin fecha"
            )

        resultado.append(
            data
        )

    return resultado

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