# ==========================================
# FORMULARIO LAVADERO
# ==========================================
@lavadero_bp.route(
    "/lavadero"
)
@login_required
def lavadero():

    lavados = listar_lavados()

    return render_template(

        "lavadero.html",

        lavados=lavados
    )


# ==========================================
# REGISTRAR LAVADO AJAX
# ==========================================
@lavadero_bp.route(
    "/registrar_lavado",
    methods=["POST"]
)
@login_required
def registrar_lavado_ajax():

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

    fecha_db = (
        datetime.utcnow()
        - timedelta(hours=5)
    ).strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    registrar_lavado(

        placa,

        vehiculo,

        tipo_lavado,

        valor,

        responsable,

        fecha_db
    )

    fecha_ticket = (
        datetime.utcnow()
        - timedelta(hours=5)
    ).strftime(
        "%d/%m/%Y %H:%M"
    )

    return {

        "success": True,

        "placa": placa,

        "vehiculo": vehiculo,

        "tipo_lavado": tipo_lavado,

        "responsable": responsable,

        "valor": f"{valor:,}",

        "fecha": fecha_ticket
    }