import math

from datetime import datetime

from config import Config


def calcular_valor(tipo, hora_ingreso):

    if isinstance(hora_ingreso, str):

        hora_ingreso = datetime.fromisoformat(hora_ingreso)

    tiempo = datetime.now() - hora_ingreso

    horas = tiempo.total_seconds() / 3600

    horas_cobradas = math.ceil(horas)

    if tipo == "Moto":

        valor = horas_cobradas * Config.TARIFA_MOTO

    else:

        valor = horas_cobradas * Config.TARIFA_CARRO

    return {
        "valor": valor,
        "horas": horas_cobradas,
        "tiempo": tiempo
    }