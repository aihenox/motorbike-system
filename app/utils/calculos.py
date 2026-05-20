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

    horas = diferencia.total_seconds() / 3600

    # ==========================================
    # COBRO POR HORA O FRACCIÓN
    # ==========================================
    horas_cobro = math.ceil(
        horas
    )

    if tipo == "Moto":

        tarifa = 1500

    else:

        tarifa = 3000

    total = horas_cobro * tarifa

    return total, ahora