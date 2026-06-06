from datetime import datetime

from flask import current_app

from zoneinfo import ZoneInfo

from app.repositories.ingreso_repository import (
    placa_activa_db,
    insertar_ingreso_db
)

from app.repositories.activos_repository import (
    obtener_vehiculo_db,
    actualizar_vehiculo_db,
    eliminar_vehiculo_db
)

from app.utils.validators import (
    validar_placa,
    validar_tipo_vehiculo
)


# ==========================================
# FECHA ACTUAL COLOMBIA
# ==========================================
def obtener_fecha_actual():

    timezone = current_app.config.get(
        "TIMEZONE",
        "America/Bogota"
    )

    return datetime.now(
        ZoneInfo(timezone)
    )


# ==========================================
# REGISTRAR INGRESO
# ==========================================
def registrar_ingreso(
    placa,
    tipo
):

    placa = validar_placa(
        placa
    )

    tipo = validar_tipo_vehiculo(
        tipo
    )

    if placa_activa_db(placa):

        return {
            "success": False,
            "message": "Vehículo ya está dentro"
        }

    hora_actual = obtener_fecha_actual()

    ticket = insertar_ingreso_db(

        placa,

        tipo,

        hora_actual.isoformat()
    )

    return {

        "success": True,

        "ticket": ticket,

        "placa": placa,

        "tipo": tipo,

        "hora": hora_actual.strftime(
            "%d/%m/%Y %I:%M %p"
        )
    }


# ==========================================
# OBTENER VEHÍCULO
# ==========================================
def obtener_vehiculo(id):

    return obtener_vehiculo_db(id)


# ==========================================
# EDITAR VEHÍCULO
# ==========================================
def editar_vehiculo(
    id,
    placa,
    tipo
):

    placa = validar_placa(
        placa
    )

    tipo = validar_tipo_vehiculo(
        tipo
    )

    actualizar_vehiculo_db(

        id,

        placa,

        tipo
    )


# ==========================================
# ELIMINAR VEHÍCULO
# ==========================================
def eliminar_vehiculo(id):

    eliminar_vehiculo_db(id)


# ==========================================
# COMPATIBILIDAD LEGACY
# ==========================================
def borrar_vehiculo(id):

    eliminar_vehiculo(id)