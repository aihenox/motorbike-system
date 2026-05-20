from datetime import datetime
from zoneinfo import ZoneInfo

import math


# ==========================================
# CALCULAR VALOR PARQUEADERO
# ==========================================
def calcular_valor(
    tipo,
    hora_ingreso
):

    # ==========================================
    # SQLITE = STRING
    # POSTGRES = DATETIME
    # ==========================================
    if isinstance(
        hora_ingreso,
        str
    ):

        hora_ingreso = datetime.fromisoformat(
            hora_ingreso
        )

    # ==========================================
    # AGREGAR TZ SI NO EXISTE
    # ==========================================
    if hora_ingreso.tzinfo is None:

        hora_ingreso = hora_ingreso.replace(
            tzinfo=ZoneInfo(
                "America/Bogota"
            )
        )

    # ==========================================
    # HORA ACTUAL COLOMBIA
    # ==========================================
    ahora = datetime.now(
        ZoneInfo("America/Bogota")
    )

    diferencia = ahora - hora_ingreso

    total_segundos = int(
        diferencia.total_seconds()
    )

    horas = total_segundos // 3600

    minutos = (
        total_segundos % 3600
    ) // 60

    # ==========================================
    # REGLA COBRO
    # SOLO COBRA SIGUIENTE HORA
    # SI SUPERA 10 MINUTOS
    # ==========================================
    horas_cobro = horas

    if minutos >= 10:

        horas_cobro += 1

    # ==========================================
    # MÍNIMO 1 HORA
    # ==========================================
    if horas_cobro <= 0:

        horas_cobro = 1

    # ==========================================
    # TARIFAS
    # ==========================================
    if tipo == "Moto":

        tarifa = 1500

    else:

        tarifa = 3000

    total = horas_cobro * tarifa

    return total, ahora