from flask import jsonify
from datetime import datetime
from zoneinfo import ZoneInfo

from flask_login import current_user

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

from app.services.cafeteria_service import (

    listar_productos_cafeteria,

    crear_producto_cafeteria,

    obtener_producto_cafeteria,

    actualizar_producto_cafeteria,

    eliminar_producto_cafeteria,

    obtener_inventario_actual,

    obtener_total_ventas_hoy,

    obtener_productos_vendidos_hoy,

    registrar_venta_cafeteria

)


cafeteria_bp = Blueprint(

    "cafeteria",

    __name__

)

# ==========================================
# DASHBOARD CAFETERIA
# ==========================================
@cafeteria_bp.route(
    "/dashboard/cafeteria"
)
@login_required
def dashboard_cafeteria():

    inventario = obtener_inventario_actual()

    vendidos_hoy = obtener_productos_vendidos_hoy()

    total_ventas_hoy = obtener_total_ventas_hoy()

    productos = listar_productos_cafeteria()

    return render_template(

        "cafeteria.html",

        inventario=inventario,

        vendidos_hoy=vendidos_hoy,

        total_ventas_hoy=total_ventas_hoy,

        productos=productos

    )

# ==========================================
# LISTADO PRODUCTOS
# ==========================================
@cafeteria_bp.route(
    "/cafeteria/configuracion"
)
@login_required
def configuracion_cafeteria():

    productos = listar_productos_cafeteria()

    return render_template(

        "cafeteria_configuracion.html",

        productos=productos
    )


# ==========================================
# NUEVO PRODUCTO
# ==========================================
@cafeteria_bp.route(

    "/cafeteria/producto/nuevo",

    methods=["GET", "POST"]
)
@login_required
def nuevo_producto():

    if request.method == "POST":

        crear_producto_cafeteria(

            request.form["nombre"],

            request.form["precio"],

            request.form["inventario"],

            request.form["stock_minimo"],

            request.form["estado"]

        )

        flash(

            "Producto creado correctamente",

            "success"

        )

        return redirect(

            url_for(
                "cafeteria.configuracion_cafeteria"
            )
        )

    return render_template(

        "cafeteria_producto_form.html"
    )


# ==========================================
# EDITAR PRODUCTO
# ==========================================
@cafeteria_bp.route(

    "/cafeteria/producto/editar/<int:producto_id>",

    methods=["GET", "POST"]
)
@login_required
def editar_producto(
    producto_id
):

    producto = obtener_producto_cafeteria(
        producto_id
    )

    if request.method == "POST":

        actualizar_producto_cafeteria(

            producto_id,

            request.form["nombre"],

            request.form["precio"],

            request.form["inventario"],

            request.form["stock_minimo"],

            request.form["estado"]

        )

        flash(

            "Producto actualizado correctamente",

            "success"

        )

        return redirect(

            url_for(
                "cafeteria.configuracion_cafeteria"
            )
        )

    return render_template(

        "cafeteria_producto_form.html",

        producto=producto

    )


# ==========================================
# ELIMINAR PRODUCTO
# ==========================================
@cafeteria_bp.route(
    "/cafeteria/producto/eliminar/<int:producto_id>"
)
@login_required
def eliminar_producto(
    producto_id
):

    eliminar_producto_cafeteria(
        producto_id
    )

    flash(

        "Producto eliminado correctamente",

        "success"

    )

    return redirect(

        url_for(
            "cafeteria.configuracion_cafeteria"
        )
    )

# ==========================================
# REGISTRAR VENTA AJAX
# ==========================================
@cafeteria_bp.route(
    "/registrar_venta",
    methods=["POST"]
)
@login_required
def registrar_venta_ajax():

    try:

        producto_id = request.form.get(
            "producto_id"
        )

        cantidad = request.form.get(
            "cantidad"
        )

        placa = request.form.get(
            "placa",
            ""
        )

        ahora = datetime.now(
            ZoneInfo(
                "America/Bogota"
            )
        )

        fecha_db = ahora.strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        resultado = registrar_venta_cafeteria(

            producto_id,

            cantidad,

            placa,

            current_user.usuario,

            fecha_db
        )

        return jsonify({

            "success": True,

            "producto": resultado["producto"],

            "cantidad": resultado["cantidad"],

            "valor_unitario": resultado["valor_unitario"],

            "total": resultado["total"],

            "inventario_restante":
                resultado[
                    "inventario_restante"
                ]
        })

    except ValueError as e:

        return jsonify({

            "success": False,

            "message": str(e)

        }), 400

    except Exception:

        return jsonify({

            "success": False,

            "message":
                "Error interno del sistema"

        }), 500