from datetime import datetime


# ==========================================
# FORMATEAR FECHA
# ==========================================
def formatear_fecha(
    fecha_str
):

    if not fecha_str:

        return "-"

    try:

        fecha = datetime.fromisoformat(
            fecha_str
        )

        return fecha.strftime(
            "%d/%m/%Y %H:%M"
        )

    except:

        return fecha_str


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

        ingreso = datetime.fromisoformat(
            hora_ingreso
        )

        if hora_salida:

            salida = datetime.fromisoformat(
                hora_salida
            )

        else:

            salida = datetime.now()

        diferencia = salida - ingreso

        total_segundos = int(
            diferencia.total_seconds()
        )

        horas = total_segundos // 3600

        minutos = (
            total_segundos % 3600
        ) // 60

        return f"{horas:02d}:{minutos:02d}"

    except:

        return "-"