from datetime import datetime
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
# REGISTRAR INGRESO
# ==========================================
def registrar_ingreso(
    placa,
    tipo
):

    placa = validar_placa(placa)

    tipo = validar_tipo_vehiculo(tipo)

    if placa_activa_db(placa):

        return {

            "success": False,

            "message": "Vehículo ya está dentro"
        }

    hora_actual = datetime.now(
        ZoneInfo("America/Bogota")
    )

    hora = hora_actual.strftime(
        "%d/%m/%Y %I:%M %p"
    )

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

        "hora": hora
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