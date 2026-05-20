from datetime import datetime

from app.repositories.ingreso_repository import (
    placa_activa_db,
    insertar_ingreso_db
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

    hora = datetime.now().strftime(
        "%d/%m/%Y %I:%M %p"
    )

    ticket = insertar_ingreso_db(

        placa,

        tipo,

        datetime.now().isoformat()
    )

    return {

        "success": True,

        "ticket": ticket,

        "placa": placa,

        "tipo": tipo,

        "hora": hora
    }