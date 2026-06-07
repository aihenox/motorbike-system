from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from flask_login import (
    login_required
)

from app.services.mensualidades_service import (
    listar_mensualidades,
    crear_mensualidad
)


mensualidades_bp = Blueprint(
    "mensualidades",
    __name__
)


# ==========================================
# LISTADO MENSUALIDADES
# ==========================================
@mensualidades_bp.route(
    "/mensualidades"
)
@login_required
def mensualidades():

    registros = listar_mensualidades()

    return render_template(

        "mensualidades.html",

        registros=registros
    )

# ==========================================
# NUEVA MENSUALIDAD
# ==========================================
@mensualidades_bp.route(
    "/mensualidades/nuevo",
    methods=["GET", "POST"]
)
@login_required
def nueva_mensualidad():

    if request.method == "POST":

        crear_mensualidad(

            request.form["placa"],

            request.form["tipo"],

            request.form["propietario"],

            request.form["telefono"],

            request.form["fecha_inicio"],

            request.form["fecha_fin"],

            request.form["estado"]
        )

        flash(
            "Mensualidad registrada correctamente"
        )

        return redirect(
            url_for(
                "mensualidades.mensualidades"
            )
        )

    return render_template(
        "mensualidad_form.html"
    )