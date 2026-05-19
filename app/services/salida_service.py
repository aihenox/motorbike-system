from datetime import datetime

import threading

from app.repositories.ingreso_repository import (
    obtener_ticket_activo_db,
    cerrar_ticket_db
)

from app.utils.calculos import calcular_valor

from app.services.pdf.pdf_generator import (
    generar_recibo_salida
)


# ==========================================
# PDF SEGUNDO PLANO
# ==========================================
def generar_pdf_salida_background(

    ticket,
    placa,
    tipo,
    hora_ingreso,
    hora_salida,
    tiempo,
    valor
):

    try:

        generar_recibo_salida(

            ticket=ticket,

            placa=placa,

            tipo=tipo,

            hora_ingreso=hora_ingreso,

            hora_salida=hora_salida,

            tiempo=tiempo,

            valor=valor
        )

    except Exception as e:

        print(
            f"Error generando PDF salida: {e}"
        )


# ==========================================
# PROCESAR SALIDA
# ==========================================
def procesar_salida(ticket):

    data = obtener_ticket_activo_db(ticket)

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

    hora_salida_texto = hora_salida.strftime(
        "%d/%m/%Y %H:%M:%S"
    )

    cerrar_ticket_db(

        ticket,

        hora_salida_texto,

        valor
    )

    # ==========================================
    # PDF SEGUNDO PLANO
    # ==========================================
    threading.Thread(

        target=generar_pdf_salida_background,

        args=(

            ticket,

            placa,

            tipo,

            ingreso_dt.strftime(
                "%d/%m/%Y %I:%M %p"
            ),

            hora_salida.strftime(
                "%d/%m/%Y %I:%M %p"
            ),

            tiempo,

            valor
        )

    ).start()

    return {

        "success": True,

        "valor": valor,

        "pdf": f"salida_{ticket}.pdf"
    }