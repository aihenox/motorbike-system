from datetime import datetime
from zoneinfo import ZoneInfo

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

        # ==========================================
        # SQLITE = STRING
        # POSTGRES = DATETIME
        # ==========================================
        hora_ingreso = item["hora_ingreso"]

        if isinstance(
            hora_ingreso,
            str
        ):

            hora_ingreso = datetime.fromisoformat(
                hora_ingreso
            )

        # ==========================================
        # HORA ACTUAL COLOMBIA
        # ==========================================
        ahora = datetime.now(
            ZoneInfo("America/Bogota")
        )

        # ==========================================
        # CONVERTIR SI NO TIENE TZ
        # ==========================================
        if hora_ingreso.tzinfo is None:

            hora_ingreso = hora_ingreso.replace(
                tzinfo=ZoneInfo(
                    "America/Bogota"
                )
            )

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

            "modalidad": item["modalidad"],

            "puesto_casco": item["puesto_casco"],

            "cantidad_cascos": item["cantidad_cascos"],

            "fecha": hora_ingreso.strftime(
                "%d/%m/%Y"
            ),

            "hora": hora_ingreso.strftime(
                "%I:%M %p"
            ),

            "tiempo": tiempo
        })
        
    return activos