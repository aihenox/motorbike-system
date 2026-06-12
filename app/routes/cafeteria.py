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
        ).strip().upper()

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

            current_user.id,

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
    
# ==========================================
# CREAR PRODUCTO AJAX
# ==========================================
@cafeteria_bp.route(
    "/cafeteria/api/crear",
    methods=["POST"]
)
@login_required
def crear_producto_ajax():

    try:

        crear_producto_cafeteria(

            request.form["nombre"],

            request.form["precio"],

            request.form["inventario"],

            request.form["stock_minimo"],

            request.form["estado"]

        )

        return jsonify({

            "success": True

        })

    except ValueError as e:

        return jsonify({

            "success": False,

            "message": str(e)

        }), 400

    except Exception:

        return jsonify({

            "success": False,

            "message": "Error interno"

        }), 500
    
# ==========================================
# OBTENER PRODUCTO AJAX
# ==========================================
@cafeteria_bp.route(
    "/cafeteria/api/producto/<int:producto_id>"
)
@login_required
def obtener_producto_ajax(
    producto_id
):

    producto = obtener_producto_cafeteria(
        producto_id
    )

    if not producto:

        return jsonify({

            "success": False

        }), 404

    if isinstance(
        producto,
        dict
    ):

        data = producto

    else:

        data = dict(producto)

    return jsonify({

        "success": True,

        "producto": data

    })

# ==========================================
# ACTUALIZAR PRODUCTO AJAX
# ==========================================
@cafeteria_bp.route(
    "/cafeteria/api/editar",
    methods=["POST"]
)
@login_required
def editar_producto_ajax():

    try:

        actualizar_producto_cafeteria(

            request.form["producto_id"],

            request.form["nombre"],

            request.form["precio"],

            request.form["inventario"],

            request.form["stock_minimo"],

            request.form["estado"]

        )

        return jsonify({

            "success": True

        })

    except ValueError as e:

        return jsonify({

            "success": False,

            "message": str(e)

        }), 400

    except Exception:

        return jsonify({

            "success": False,

            "message": "Error interno"

        }), 500
    
# ==========================================
# ELIMINAR PRODUCTO AJAX
# ==========================================
@cafeteria_bp.route(
    "/cafeteria/api/eliminar/<int:producto_id>",
    methods=["DELETE"]
)
@login_required
def eliminar_producto_ajax(
    producto_id
):

    try:

        eliminar_producto_cafeteria(
            producto_id
        )

        return jsonify({

            "success": True

        })

    except Exception as e:

        return jsonify({

            "success": False,

            "message": str(e)

        }), 500