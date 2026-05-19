from flask import (
    Blueprint,
    render_template,
    request,
    send_file
)

from flask_login import login_required

from app.services.historial_service import (

    listar_historial,

    buscar_placa,

    filtrar_fecha
)

from openpyxl import Workbook

from openpyxl.styles import Font

from io import BytesIO


historial_bp = Blueprint(
    "historial",
    __name__
)


# ==========================================
# OBTENER DATOS FILTRADOS
# ==========================================
def obtener_datos_filtrados(
    placa,
    fecha
):

    # FECHA
    if fecha:

        return filtrar_fecha(
            fecha
        )

    # PLACA
    if placa:

        return buscar_placa(
            placa
        )

    # TODO
    return listar_historial()


# ==========================================
# HISTORIAL
# ==========================================
@historial_bp.route("/historial")
@login_required
def historial():

    placa = request.args.get(
        "placa",
        ""
    )

    fecha = request.args.get(
        "fecha",
        ""
    )

    historial_data = obtener_datos_filtrados(
        placa,
        fecha
    )

    total = sum(

        item["valor"] or 0

        for item in historial_data
    )

    return render_template(

        "historial.html",

        historial=historial_data,

        total=total,

        placa=placa,

        fecha=fecha
    )


# ==========================================
# EXPORTAR EXCEL
# ==========================================
@historial_bp.route("/historial/excel")
@login_required
def exportar_excel():

    placa = request.args.get(
        "placa",
        ""
    )

    fecha = request.args.get(
        "fecha",
        ""
    )

    historial_data = obtener_datos_filtrados(
        placa,
        fecha
    )

    wb = Workbook()

    ws = wb.active

    ws.title = "Historial"

    headers = [

        "ID",

        "Fecha",

        "Vehículo",

        "Placa",

        "Hora entrada",

        "Hora salida",

        "Tiempo",

        "Total",

        "Estado"
    ]

    ws.append(headers)

    # ESTILO HEADERS
    for cell in ws[1]:

        cell.font = Font(
            bold=True
        )

    # DATOS
    for item in historial_data:

        fecha_ingreso = item[
            "hora_ingreso"
        ].split(" ")

        fecha = fecha_ingreso[0]

        hora_entrada = (
            fecha_ingreso[1]
            if len(fecha_ingreso) > 1
            else "-"
        )

        if item["hora_salida"] != "-":

            hora_salida = item[
                "hora_salida"
            ].split(" ")[1]

        else:

            hora_salida = "-"

        ws.append([

            item["id"],

            fecha,

            item["tipo"],

            item["placa"],

            hora_entrada,

            hora_salida,

            item[
                "tiempo_transcurrido"
            ],

            item["valor"] or 0,

            item["estado"]
        ])

    # AJUSTAR COLUMNAS
    for column in ws.columns:

        max_length = 0

        column_letter = column[0].column_letter

        for cell in column:

            try:

                if len(str(cell.value)) > max_length:

                    max_length = len(
                        str(cell.value)
                    )

            except:
                pass

        adjusted_width = (
            max_length + 4
        )

        ws.column_dimensions[
            column_letter
        ].width = adjusted_width

    # MEMORIA
    output = BytesIO()

    wb.save(output)

    output.seek(0)

    return send_file(

        output,

        as_attachment=True,

        download_name="historial.xlsx",

        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )