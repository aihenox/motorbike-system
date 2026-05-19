from datetime import datetime
import math

def calcular_valor(tipo, hora_ingreso):
    hora_ingreso = datetime.fromisoformat(hora_ingreso)
    ahora = datetime.now()

    diferencia = ahora - hora_ingreso
    horas = diferencia.total_seconds() / 3600

    # cobra hora o fracción
    horas_cobro = math.ceil(horas)

    if tipo == "Moto":
        tarifa = 1500
    else:
        tarifa = 3000

    total = horas_cobro * tarifa

    return total, ahora