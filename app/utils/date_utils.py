from datetime import datetime
from zoneinfo import ZoneInfo


BOGOTA_TZ = ZoneInfo("America/Bogota")


# ==========================================
# PARSEAR FECHA
# ==========================================
def parsear_fecha(fecha):

    if not fecha:

        return None

    if not isinstance(fecha, str):

        return fecha

    for formato in (
        None,
        "%d/%m/%Y %H:%M:%S",
        "%d/%m/%Y %H:%M",
        "%d/%m/%Y %I:%M %p"
    ):

        try:

            if formato is None:

                return datetime.fromisoformat(fecha)

            return datetime.strptime(
                fecha,
                formato
            )

        except ValueError:

            continue

    raise ValueError(
        f"Formato de fecha no soportado: {fecha}"
    )


def asegurar_zona_colombia(fecha):

    if fecha.tzinfo is None:

        return fecha.replace(
            tzinfo=BOGOTA_TZ
        )

    return fecha.astimezone(
        BOGOTA_TZ
    )


# ==========================================
# FORMATEAR FECHA
# ==========================================
def formatear_fecha(
    fecha_str
):

    if not fecha_str:

        return "-"

    try:

        fecha = parsear_fecha(
            fecha_str
        )

        return fecha.strftime(
            "%d/%m/%Y %H:%M"
        )

    except:

        return str(fecha_str)


# ==========================================
# TIEMPO TRANSCURRIDO
# ==========================================
def calcular_tiempo_transcurrido(

    hora_ingreso,

    hora_salida=None
):

    if not hora_ingreso:

        return "-"

    try:

        ingreso = parsear_fecha(
            hora_ingreso
        )

        # ==========================================
        # SALIDA
        # ==========================================
        if hora_salida:

            salida = parsear_fecha(
                hora_salida
            )

        else:

            salida = datetime.now(
                BOGOTA_TZ
            )

        # ==========================================
        # TIMEZONE
        # ==========================================
        ingreso = asegurar_zona_colombia(
            ingreso
        )

        salida = asegurar_zona_colombia(
            salida
        )

        diferencia = salida - ingreso

        total_segundos = int(
            diferencia.total_seconds()
        )

        horas = total_segundos // 3600

        minutos = (
            total_segundos % 3600
        ) // 60

        # ==========================================
        # FORMATO
        # ==========================================
        return f"{horas}h {minutos}m"

    except:

        return "-"
