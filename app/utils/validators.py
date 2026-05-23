# app/utils/validators.py

from datetime import datetime


def validar_placa(placa):
    """
    Valida y normaliza una placa.
    Retorna la placa limpia en mayúsculas.
    """

    if placa is None:
        raise ValueError("La placa es obligatoria")

    placa = placa.strip().upper()

    if not placa:
        raise ValueError("La placa es obligatoria")

    if not placa.isalnum():
        raise ValueError(
            "La placa solo puede contener letras y números"
        )

    if len(placa) < 5:
        raise ValueError(
            "La placa debe tener mínimo 5 caracteres"
        )

    if len(placa) > 10:
        raise ValueError(
            "La placa excede la longitud permitida"
        )

    return placa


def validar_tipo_vehiculo(tipo):

    if tipo is None:
        raise ValueError(
            "Debe seleccionar un tipo de vehículo"
        )

    tipo = tipo.strip().lower()

    tipos_validos = {
        "moto",
        "carro"
    }

    if tipo not in tipos_validos:
        raise ValueError(
            "Tipo de vehículo inválido"
        )

    return tipo.capitalize()

def validar_valor(valor):
    """
    Valida valores monetarios.
    """

    try:
        valor = float(valor)

    except (ValueError, TypeError):
        raise ValueError(
            "Debe ingresar un valor numérico válido"
        )

    if valor < 0:
        raise ValueError(
            "El valor no puede ser negativo"
        )

    return valor


def validar_texto(texto, campo="Campo"):
    """
    Valida textos obligatorios.
    """

    if texto is None:
        raise ValueError(
            f"{campo} es obligatorio"
        )

    texto = texto.strip()

    if not texto:
        raise ValueError(
            f"{campo} es obligatorio"
        )

    return texto


def validar_fecha(fecha):
    """
    Valida fechas en formato YYYY-MM-DD.
    """

    if not fecha:
        raise ValueError(
            "La fecha es obligatoria"
        )

    try:
        datetime.strptime(
            fecha,
            "%Y-%m-%d"
        )

    except ValueError:
        raise ValueError(
            "Formato de fecha inválido"
        )

    return fecha


def validar_rango_fechas(
    fecha_inicio,
    fecha_fin
):
    """
    Valida rangos de fechas.
    """

    fecha_inicio = validar_fecha(
        fecha_inicio
    )

    fecha_fin = validar_fecha(
        fecha_fin
    )

    inicio = datetime.strptime(
        fecha_inicio,
        "%Y-%m-%d"
    )

    fin = datetime.strptime(
        fecha_fin,
        "%Y-%m-%d"
    )

    if inicio > fin:
        raise ValueError(
            "La fecha inicial no puede ser mayor que la fecha final"
        )

    return fecha_inicio, fecha_fin


def validar_id(registro_id):
    """
    Valida IDs numéricos.
    """

    try:
        registro_id = int(registro_id)

    except (ValueError, TypeError):
        raise ValueError(
            "Identificador inválido"
        )

    if registro_id <= 0:
        raise ValueError(
            "Identificador inválido"
        )

    return registro_id

def validar_responsable(responsable):

    if not responsable:
        raise ValueError(
            "Debe seleccionar un responsable"
        )

    responsables_validos = {
        "Angela",
        "Angelica",
        "Diva",
        "Karime"
    }

    if responsable not in responsables_validos:
        raise ValueError(
            "Responsable inválido"
        )

    return responsable

def validar_tipo_lavado(tipo):

    if not tipo:
        raise ValueError(
            "Debe ingresar el servicio realizado"
        )

    tipo = tipo.strip()

    if len(tipo) < 3:
        raise ValueError(
            "Servicio inválido"
        )

    return tipo