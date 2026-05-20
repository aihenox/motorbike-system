from datetime import datetime
from zoneinfo import ZoneInfo

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

    # ==========================================
    # SQLITE = STRING
    # POSTGRES = DATETIME
    # ==========================================
    if isinstance(
        hora_ingreso,
        str
    ):

        ingreso_dt = datetime.fromisoformat(
            hora_ingreso
        )

    else:

        ingreso_dt = hora_ingreso

    # ==========================================
    # AGREGAR TZ SI NO EXISTE
    # ==========================================
    if ingreso_dt.tzinfo is None:

        ingreso_dt = ingreso_dt.replace(
            tzinfo=ZoneInfo(
                "America/Bogota"
            )
        )

    # ==========================================
    # CALCULAR VALOR
    # ==========================================
    valor, hora_salida = calcular_valor(

        tipo,

        ingreso_dt.isoformat()
    )

    # ==========================================
    # ASEGURAR TZ EN SALIDA
    # ==========================================
    if hora_salida.tzinfo is None:

        hora_salida = hora_salida.replace(
            tzinfo=ZoneInfo(
                "America/Bogota"
            )
        )

    # ==========================================
    # DIFERENCIA TIEMPO
    # ==========================================
    diferencia = hora_salida - ingreso_dt

    dias = diferencia.days

    horas = diferencia.seconds // 3600

    minutos = (
        diferencia.seconds % 3600
    ) // 60

    tiempo = ""

    if dias > 0:

        tiempo += f"{dias}d "

    tiempo += f"{horas:02d}:{minutos:02d}"

    # ==========================================
    # CERRAR TICKET
    # ==========================================
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