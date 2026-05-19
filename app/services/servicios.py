from datetime import datetime

from app.repositories.ingreso_repository import (
    placa_activa_db,
    insertar_ingreso_db,
    obtener_ticket_activo_db,
    cerrar_ticket_db
)

from recibo import generar_recibo

from logica import calcular_valor


# ==========================================
# REGISTRAR INGRESO
# ==========================================
def registrar_ingreso(placa, tipo):

    placa = placa.upper().strip()

    if placa_activa_db(placa):

        return False, "Vehículo ya está dentro"

    hora = datetime.now().isoformat()

    ticket = insertar_ingreso_db(
        placa,
        tipo,
        hora
    )

    generar_recibo(
        ticket,
        placa,
        tipo,
        hora
    )

    return True, ticket


# ==========================================
# REGISTRAR SALIDA
# ==========================================
def registrar_salida(ticket):

    data = obtener_ticket_activo_db(ticket)

    if not data:

        return False, "Ticket inválido"

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

    return True, valor