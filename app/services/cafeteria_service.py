from app.repositories.cafeteria_repository import (

    obtener_productos_cafeteria_db,

    crear_producto_cafeteria_db,

    obtener_producto_cafeteria_db,

    actualizar_producto_cafeteria_db,

    eliminar_producto_cafeteria_db,

    obtener_inventario_actual_db,

    obtener_total_ventas_hoy_db,

    obtener_productos_vendidos_hoy_db,

    registrar_venta_cafeteria_db
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
# REGISTRAR VENTA
# ==========================================
def registrar_venta_cafeteria(

    producto_id,

    cantidad,

    placa,

    usuario,

    fecha

):

    producto_id = validar_id(
        producto_id
    )

    cantidad = int(
        validar_valor(
            cantidad
        )
    )

    if cantidad <= 0:

        raise ValueError(
            "La cantidad debe ser mayor a cero"
        )

    producto = obtener_producto_cafeteria_db(
        producto_id
    )

    if not producto:

        raise ValueError(
            "Producto no encontrado"
        )

    inventario = producto["inventario"]

    if inventario < cantidad:

        raise ValueError(

            f"Inventario insuficiente. Disponible: {inventario}"

        )

    valor_unitario = producto["precio"]

    total = valor_unitario * cantidad

    registrar_venta_cafeteria_db(

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

        "producto": producto["nombre"],

        "cantidad": cantidad,

        "valor_unitario": valor_unitario,

        "total": total,

        "inventario_restante": (

            inventario - cantidad

        )

    }