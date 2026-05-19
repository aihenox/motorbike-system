from datetime import datetime

from app.repositories.activos_repository import (
    obtener_activos_db
)


# ==========================================
# LISTAR ACTIVOS
# ==========================================
def listar_activos():

    activos_db = obtener_activos_db()

    activos = []

    for item in activos_db:

        hora_ingreso = datetime.fromisoformat(
            item["hora_ingreso"]
        )

        ahora = datetime.now()

        diferencia = ahora - hora_ingreso

        dias = diferencia.days

        horas = diferencia.seconds // 3600

        minutos = (
            diferencia.seconds % 3600
        ) // 60

        tiempo = ""

        if dias > 0:

            tiempo += f"{dias}d "

        tiempo += f"{horas}h {minutos}m"

        activos.append({

            "id": item["id"],

            "placa": item["placa"],

            "tipo": item["tipo"],

            "fecha": hora_ingreso.strftime(
                "%d/%m/%Y"
            ),

            "hora": hora_ingreso.strftime(
                "%I:%M %p"
            ),

            "tiempo": tiempo
        })

    return activos