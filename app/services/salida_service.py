from datetime import datetime

from app.repositories.ingreso_repository import (
    obtener_ticket_activo_db,
    cerrar_ticket_db
)

from app.utils.calculos import (
    calcular_valor
)


# ==========================================
# PROCESAR SALIDA
# ==========================================
def procesar_salida(ticket):

    data = obtener_ticket_activo_db(
        ticket
    )

    if not data:

        return {

            "success": False,

            "message": "Ticket inválido"
        }

    tipo = data["tipo"]

    placa = data["placa"]

    hora_ingreso = data["hora_ingreso"]

    valor, hora_salida = calcular_valor(

        tipo,

        hora_ingreso
    )

    ingreso_dt = datetime.fromisoformat(
        hora_ingreso
    )

    diferencia = hora_salida - ingreso_dt

    horas = diferencia.seconds // 3600

    minutos = (
        diferencia.seconds % 3600
    ) // 60

    tiempo = f"{horas:02d}:{minutos:02d}"

    cerrar_ticket_db(

        ticket,

        hora_salida.strftime(
            "%d/%m/%Y %H:%M:%S"
        ),

        valor
    )

    return {

        "success": True,

        "ticket": ticket,

        "placa": placa,

        "tipo": tipo,

        "hora_ingreso": ingreso_dt.strftime(
            "%d/%m/%Y %I:%M %p"
        ),

        "hora_salida": hora_salida.strftime(
            "%d/%m/%Y %I:%M %p"
        ),

        "tiempo": tiempo,

        "valor": valor
    }