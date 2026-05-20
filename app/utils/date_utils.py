from datetime import datetime
from zoneinfo import ZoneInfo


# ==========================================
# FORMATEAR FECHA
# ==========================================
def formatear_fecha(
    fecha_str
):

    if not fecha_str:

        return "-"

    try:

        # ==========================================
        # SQLITE = STRING
        # POSTGRES = DATETIME
        # ==========================================
        if isinstance(
            fecha_str,
            str
        ):

            fecha = datetime.fromisoformat(
                fecha_str
            )

        else:

            fecha = fecha_str

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

        # ==========================================
        # INGRESO
        # ==========================================
        if isinstance(
            hora_ingreso,
            str
        ):

            ingreso = datetime.fromisoformat(
                hora_ingreso
            )

        else:

            ingreso = hora_ingreso

        # ==========================================
        # SALIDA
        # ==========================================
        if hora_salida:

            if isinstance(
                hora_salida,
                str
            ):

                salida = datetime.fromisoformat(
                    hora_salida
                )

            else:

                salida = hora_salida

        else:

            salida = datetime.now(
                ZoneInfo(
                    "America/Bogota"
                )
            )

        # ==========================================
        # TIMEZONE
        # ==========================================
        if ingreso.tzinfo is None:

            ingreso = ingreso.replace(
                tzinfo=ZoneInfo(
                    "America/Bogota"
                )
            )

        if salida.tzinfo is None:

            salida = salida.replace(
                tzinfo=ZoneInfo(
                    "America/Bogota"
                )
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