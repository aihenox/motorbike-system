from flask import (

    Blueprint,

    render_template,

    request,

    redirect,

    url_for,

    send_file
)

import openpyxl

from io import BytesIO

from datetime import datetime

from flask_login import (
    login_required
)

from app.services.lavadero_service import (

    registrar_lavado,

    listar_lavados,

    obtener_metricas_lavadero,

    obtener_estadisticas_responsables,

    obtener_lavado_por_id,

    actualizar_lavado
)

from app.services.historial_lavadero_service import (

    listar_historial_lavadero,

    obtener_total_lavadero
)


lavadero_bp = Blueprint(
    "lavadero",
    __name__
)


# ==========================================
# DASHBOARD LAVADERO
# ==========================================
@lavadero_bp.route(
    "/dashboard/lavadero"
)
@login_required
def dashboard_lavadero():

    metricas = obtener_metricas_lavadero()

    lavados = listar_lavados()

    estadisticas = (
        obtener_estadisticas_responsables()
    )

    return render_template(

        "dashboard_lavadero.html",

        lavados_motos=metricas.get(
            "lavados_motos",
            0
        ),

        lavados_carros=metricas.get(
            "lavados_carros",
            0
        ),

        total_servicios=metricas.get(
            "dinero_generado",
            0
        ),

        lavados=lavados,

        estadisticas=estadisticas
    )


# ==========================================
# REGISTRO LAVADOS
# ==========================================
@lavadero_bp.route(

    "/lavadero",

    methods=["GET", "POST"]
)
@login_required
def lavadero():

    if request.method == "POST":

        placa = request.form[
            "placa"
        ].upper()

        vehiculo = request.form[
            "vehiculo"
        ]

        tipo_lavado = request.form[
            "tipo_lavado"
        ]

        valor = int(
            request.form["valor"]
        )

        responsable = request.form[
            "responsable"
        ]

        fecha = datetime.now().isoformat()

        registrar_lavado(

            placa,

            vehiculo,

            tipo_lavado,

            valor,

            responsable,

            fecha
        )

        return redirect(
            url_for(
                "lavadero.lavadero"
            )
        )

    lavados = listar_lavados()

    return render_template(

        "lavadero.html",

        lavados=lavados
    )


# ==========================================
# HISTORIAL LAVADERO
# ==========================================
@lavadero_bp.route(
    "/historial/lavadero"
)
@login_required
def historial_lavadero():

    placa = request.args.get(
        "placa",
        ""
    )

    fecha = request.args.get(
        "fecha",
        ""
    )

    responsable = request.args.get(
        "responsable",
        ""
    )

    historial = listar_historial_lavadero(

        placa,

        fecha,

        responsable
    )

    total = obtener_total_lavadero(

        placa,

        fecha,

        responsable
    )

    return render_template(

        "historial_lavadero.html",

        historial=historial,

        total=total,

        placa=placa,

        fecha=fecha,

        responsable=responsable
    )


# ==========================================
# EXPORTAR EXCEL HISTORIAL LAVADERO
# ==========================================
@lavadero_bp.route(
    "/historial/lavadero/excel"
)
@login_required
def exportar_excel_lavadero():

    placa = request.args.get(
        "placa",
        ""
    )

    fecha = request.args.get(
        "fecha",
        ""
    )

    responsable = request.args.get(
        "responsable",
        ""
    )

    historial = listar_historial_lavadero(

        placa,

        fecha,

        responsable
    )

    wb = openpyxl.Workbook()

    ws = wb.active

    ws.title = "Historial Lavadero"

    encabezados = [

        "Fecha",

        "Vehículo",

        "Placa",

        "Responsable",

        "Tipo lavado",

        "Valor"
    ]

    ws.append(
        encabezados
    )

    for item in historial:

        ws.append([

            item["fecha"],

            item["vehiculo"],

            item["placa"],

            item["responsable"],

            item["tipo_lavado"],

            item["valor"]
        ])

    for columna in ws.columns:

        longitud = 0

        columna_letra = columna[0].column_letter

        for celda in columna:

            try:

                if len(str(celda.value)) > longitud:

                    longitud = len(
                        str(celda.value)
                    )

            except:

                pass

        ws.column_dimensions[
            columna_letra
        ].width = longitud + 5

    archivo = BytesIO()

    wb.save(archivo)

    archivo.seek(0)

    return send_file(

        archivo,

        as_attachment=True,

        download_name=
        "historial_lavadero.xlsx",

        mimetype=
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )


# ==========================================
# EDITAR LAVADO
# ==========================================
@lavadero_bp.route(

    "/editar-lavado/<int:lavado_id>",

    methods=["GET", "POST"]
)
@login_required
def editar_lavado(

    lavado_id
):

    lavado = obtener_lavado_por_id(
        lavado_id
    )

    if request.method == "POST":

        placa = request.form[
            "placa"
        ].upper()

        vehiculo = request.form[
            "vehiculo"
        ]

        tipo_lavado = request.form[
            "tipo_lavado"
        ]

        valor = int(
            request.form["valor"]
        )

        responsable = request.form[
            "responsable"
        ]

        actualizar_lavado(

            lavado_id,

            placa,

            vehiculo,

            tipo_lavado,

            valor,

            responsable
        )

        return redirect(
            url_for(
                "lavadero.historial_lavadero"
            )
        )

    return render_template(

        "editar_lavado.html",

        lavado=lavado
    )