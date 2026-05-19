from datetime import datetime

from app.repositories.ingreso_repository import (
    placa_activa_db,
    insertar_ingreso_db,
    obtener_ticket_activo_db,
    cerrar_ticket_db
)

from app.repositories.activos_repository import (
    obtener_vehiculo_db,
    actualizar_vehiculo_db,
    eliminar_vehiculo_db
)

from app.utils.calculos import calcular_valor

from app.services.pdf.pdf_generator import (
    generar_recibo_ingreso
)


# ==========================================
# REGISTRAR INGRESO
# ==========================================
def registrar_ingreso(placa, tipo):

    placa = placa.upper().strip()

    if placa_activa_db(placa):

        return {
            "success": False,
            "message": "Vehículo ya está dentro"
        }

    hora = datetime.now().isoformat()

    ticket = insertar_ingreso_db(
        placa,
        tipo,
        hora
    )

    ruta_pdf = generar_recibo_ingreso(
        ticket,
        placa,
        tipo,
        hora
    )

    return {
        "success": True,
        "ticket": ticket,
        "pdf": ruta_pdf
    }


# ==========================================
# REGISTRAR SALIDA
# ==========================================
def registrar_salida(ticket):

    data = obtener_ticket_activo_db(ticket)

    if not data:

        return {
            "success": False,
            "message": "Ticket inválido"
        }

    tipo = data["tipo"]

    hora_ingreso = data["hora_ingreso"]

    valor, hora_salida = calcular_valor(
        tipo,
        hora_ingreso
    )

    cerrar_ticket_db(
        ticket,
        hora_salida.isoformat(),
        valor
    )

    return {
        "success": True,
        "valor": valor
    }


# ==========================================
# OBTENER VEHÍCULO
# ==========================================
def obtener_vehiculo(id):

    return obtener_vehiculo_db(id)


# ==========================================
# EDITAR VEHÍCULO
# ==========================================
def editar_vehiculo(id, placa, tipo):

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