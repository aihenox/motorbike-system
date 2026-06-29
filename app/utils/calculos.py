from datetime import datetime
from zoneinfo import ZoneInfo

from app.utils.date_utils import (
    asegurar_zona_colombia,
    parsear_fecha
)

from app.services.tarifas_service import (
    obtener_tarifa_activa
)


# ==========================================
# CALCULAR VALOR PARQUEADERO
# ==========================================
def calcular_valor(
    tipo,
    hora_ingreso,
    ahora=None
):

    hora_ingreso = asegurar_zona_colombia(
        parsear_fecha(
            hora_ingreso
        )
    )

    if ahora is None:

        ahora = datetime.now(
            ZoneInfo("America/Bogota")
        )

    ahora = asegurar_zona_colombia(
        ahora
    )

    diferencia = ahora - hora_ingreso

    total_segundos = int(
        diferencia.total_seconds()
    )

    if total_segundos < 0:

        raise ValueError(
            "La hora de ingreso no puede estar en el futuro"
        )

    total_minutos = total_segundos // 60

    horas = total_minutos // 60

    minutos = total_minutos % 60

    # ==========================================
    # CONFIGURACION
    # ==========================================
    tarifas = obtener_tarifa_activa()

    if not tarifas:

        raise RuntimeError(
            "No existe una configuración de tarifas activa"
        )

    
    minutos_gracia = tarifas.get(
        "minutos_gracia",
        10
    )

    horas_cobro = horas

    if minutos > minutos_gracia:

        horas_cobro += 1

    if horas_cobro <= 0:

        horas_cobro = 1

    # ==========================================
    # TARIFA SEGUN VEHICULO
    # ==========================================
    if tipo == "Moto":

        tarifa = tarifas.get(
            "hora_moto",
            1500
        )

    elif tipo == "Carro":

        tarifa = tarifas.get(
            "hora_carro",
            3000
        )

    else:

        raise ValueError(
            "Tipo de vehículo inválido"
        )

    total = horas_cobro * tarifa

    return total, ahora
