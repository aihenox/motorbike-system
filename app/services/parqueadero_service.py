from datetime import datetime

import threading

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
# GENERAR PDF ASYNC
# ==========================================
def generar_pdf_background(
    ticket,
    placa,
    tipo,
    hora
):

    try:

        generar_recibo_ingreso(
            ticket,
            placa,
            tipo,
            hora
        )

    except Exception as e:

        print(
            f"Error generando PDF ingreso: {e}"
        )


# ==========================================
# REGISTRAR INGRESO
# ==========================================
def registrar_ingreso(
    placa,
    tipo
):

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

    # ==========================================
    # PDF SEGUNDO PLANO
    # ==========================================
    threading.Thread(

        target=generar_pdf_background,

        args=(
            ticket,
            placa,
            tipo,
            hora
        )

    ).start()

    return {

        "success": True,

        "ticket": ticket,

        "pdf": f"recibo_ingreso_{ticket}.pdf"
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