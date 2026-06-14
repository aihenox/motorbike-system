from app.repositories.cafeteria_repository import (

    obtener_productos_cafeteria_db,

    crear_producto_cafeteria_db,

    obtener_producto_cafeteria_db,

    actualizar_producto_cafeteria_db,

    eliminar_producto_cafeteria_db,

    obtener_inventario_actual_db,

    obtener_total_ventas_hoy_db,

    obtener_productos_vendidos_hoy_db,

    registrar_venta_cafeteria_db,

    buscar_producto_por_nombre_db,

    obtener_consecutivo_venta_dia_db,

    obtener_resumen_ventas_hoy_db,

    obtener_historial_ventas_cafeteria_db,

    obtener_detalle_venta_cafeteria_db
)

from app.utils.validators import (

    validar_id,

    validar_texto,

    validar_valor

)


# ==========================================
# LISTAR PRODUCTOS
# ==========================================
def listar_productos_cafeteria():

    return obtener_productos_cafeteria_db()


# ==========================================
# CREAR PRODUCTO
# ==========================================
def crear_producto_cafeteria(

    nombre,

    precio,

    inventario,

    stock_minimo,

    estado

):

    nombre = validar_texto(

        nombre,

        "Nombre producto"

    )

    precio = int(

        validar_valor(
            precio
        )
    )

    inventario = int(

        validar_valor(
            inventario
        )
    )

    stock_minimo = int(

        validar_valor(
            stock_minimo
        )
    )

    producto_existente = buscar_producto_por_nombre_db(
        nombre
    )

    if producto_existente:

        if isinstance(
            producto_existente,
            dict
        ):

            producto_id = producto_existente["id"]

            inventario_actual = (
                producto_existente["inventario"]
            )

        else:

            producto_id = producto_existente["id"]

            inventario_actual = (
                producto_existente["inventario"]
            )

        actualizar_producto_cafeteria_db(

            producto_id,

            nombre,

            precio,

            inventario_actual + inventario,

            stock_minimo,

            estado

        )

        return

    crear_producto_cafeteria_db(

        nombre,

        precio,

        inventario,

        stock_minimo,

        estado

    )


# ==========================================
# OBTENER PRODUCTO
# ==========================================
def obtener_producto_cafeteria(
    producto_id
):

    producto_id = validar_id(
        producto_id
    )

    return obtener_producto_cafeteria_db(
        producto_id
    )


# ==========================================
# ACTUALIZAR PRODUCTO
# ==========================================
def actualizar_producto_cafeteria(

    producto_id,

    nombre,

    precio,

    inventario,

    stock_minimo,

    estado

):

    producto_id = validar_id(
        producto_id
    )

    nombre = validar_texto(

        nombre,

        "Nombre producto"

    )

    precio = int(

        validar_valor(
            precio
        )
    )

    inventario = int(

        validar_valor(
            inventario
        )
    )

    stock_minimo = int(

        validar_valor(
            stock_minimo
        )
    )

    actualizar_producto_cafeteria_db(

        producto_id,

        nombre,

        precio,

        inventario,

        stock_minimo,

        estado

    )


# ==========================================
# ELIMINAR PRODUCTO
# ==========================================
def eliminar_producto_cafeteria(
    producto_id
):

    producto_id = validar_id(
        producto_id
    )

    eliminar_producto_cafeteria_db(
        producto_id
    )

# ==========================================
# INVENTARIO ACTUAL
# ==========================================
def obtener_inventario_actual():

    return obtener_inventario_actual_db()


# ==========================================
# TOTAL VENTAS HOY
# ==========================================
def obtener_total_ventas_hoy():

    return obtener_total_ventas_hoy_db()


# ==========================================
# PRODUCTOS VENDIDOS HOY
# ==========================================
def obtener_productos_vendidos_hoy():

    return obtener_productos_vendidos_hoy_db()

# ==========================================
# REGISTRAR VENTA CARRITO
# ==========================================
def registrar_venta_cafeteria(

    productos,

    placa,

    usuario,

    fecha

):

    if not productos:

        raise ValueError(
            "Debe agregar al menos un producto"
        )

    # ==========================================
    # GENERAR CONSECUTIVO SI NO HAY PLACA
    # ==========================================
    if not placa:

        consecutivo = (
            obtener_consecutivo_venta_dia_db()
        )

        placa = (
            f"VENTA #{consecutivo}"
        )

    total_general = 0

    from datetime import datetime
    from zoneinfo import ZoneInfo

    venta_id = datetime.now(
        ZoneInfo(
            "America/Bogota"
        )
    ).strftime(
        "%Y%m%d%H%M%S"
    )

    for item in productos:

        producto_id = validar_id(
            item["producto_id"]
        )

        cantidad = int(
            item["cantidad"]
        )

        producto = (
            obtener_producto_cafeteria_db(
                producto_id
            )
        )

        if not producto:

            raise ValueError(
                "Producto no encontrado"
            )

        inventario = (
            producto["inventario"]
        )

        if inventario < cantidad:

            raise ValueError(

                f"Inventario insuficiente para {producto['nombre']}"

            )

        valor_unitario = (
            producto["precio"]
        )

        total = (
            valor_unitario *
            cantidad
        )

        total_general += total

        registrar_venta_cafeteria_db(

            venta_id,

            fecha,

            producto_id,

            producto["nombre"],

            cantidad,

            valor_unitario,

            total,

            placa,

            usuario

        )

    return {

        "success": True,

        "placa": placa,

        "total": total_general

    }

# ==========================================
# RESUMEN VENTAS DEL DIA
# ==========================================
def obtener_resumen_ventas_hoy():

    return obtener_resumen_ventas_hoy_db()

# ==========================================
# HISTORIAL VENTAS CAFETERIA
# ==========================================
def obtener_historial_ventas_cafeteria():

    return (
        obtener_historial_ventas_cafeteria_db()
    )

# ==========================================
# DETALLE VENTA CAFETERIA
# ==========================================
def obtener_detalle_venta_cafeteria(
    venta_id
):

    return (
        obtener_detalle_venta_cafeteria_db(
            venta_id
        )
    )