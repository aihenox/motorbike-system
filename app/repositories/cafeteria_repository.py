import os

from app.repositories.connection import conectar


# ==========================================
# MOTOR DATABASE
# ==========================================
POSTGRES = os.getenv(
    "DATABASE_URL"
)


# ==========================================
# LISTAR PRODUCTOS
# ==========================================
def obtener_productos_cafeteria_db():

    with conectar() as conn:

        c = conn.cursor()

        c.execute("""

            SELECT

                id,
                nombre,
                precio,
                inventario,
                stock_minimo,
                estado

            FROM productos_cafeteria

            ORDER BY nombre

        """)

        return c.fetchall()


# ==========================================
# CREAR PRODUCTO
# ==========================================
def crear_producto_cafeteria_db(

    nombre,

    precio,

    inventario,

    stock_minimo,

    estado
):

    with conectar() as conn:

        c = conn.cursor()

        if POSTGRES:

            c.execute("""

                INSERT INTO productos_cafeteria(

                    nombre,
                    precio,
                    inventario,
                    stock_minimo,
                    estado

                )

                VALUES(

                    %s,
                    %s,
                    %s,
                    %s,
                    %s

                )

            """, (

                nombre,

                precio,

                inventario,

                stock_minimo,

                estado

            ))

        else:

            c.execute("""

                INSERT INTO productos_cafeteria(

                    nombre,
                    precio,
                    inventario,
                    stock_minimo,
                    estado

                )

                VALUES (?, ?, ?, ?, ?)

            """, (

                nombre,

                precio,

                inventario,

                stock_minimo,

                estado

            ))

        conn.commit()


# ==========================================
# OBTENER PRODUCTO
# ==========================================
def obtener_producto_cafeteria_db(
    producto_id
):

    with conectar() as conn:

        c = conn.cursor()

        if POSTGRES:

            c.execute("""

                SELECT *

                FROM productos_cafeteria

                WHERE id = %s

            """, (
                producto_id,
            ))

        else:

            c.execute("""

                SELECT *

                FROM productos_cafeteria

                WHERE id = ?

            """, (
                producto_id,
            ))

        return c.fetchone()


# ==========================================
# ACTUALIZAR PRODUCTO
# ==========================================
def actualizar_producto_cafeteria_db(

    producto_id,

    nombre,

    precio,

    inventario,

    stock_minimo,

    estado
):

    with conectar() as conn:

        c = conn.cursor()

        if POSTGRES:

            c.execute("""

                UPDATE productos_cafeteria

                SET

                    nombre = %s,
                    precio = %s,
                    inventario = %s,
                    stock_minimo = %s,
                    estado = %s

                WHERE id = %s

            """, (

                nombre,

                precio,

                inventario,

                stock_minimo,

                estado,

                producto_id

            ))

        else:

            c.execute("""

                UPDATE productos_cafeteria

                SET

                    nombre = ?,
                    precio = ?,
                    inventario = ?,
                    stock_minimo = ?,
                    estado = ?

                WHERE id = ?

            """, (

                nombre,

                precio,

                inventario,

                stock_minimo,

                estado,

                producto_id

            ))

        conn.commit()


# ==========================================
# ELIMINAR PRODUCTO
# ==========================================
def eliminar_producto_cafeteria_db(
    producto_id
):

    with conectar() as conn:

        c = conn.cursor()

        if POSTGRES:

            c.execute("""

                DELETE

                FROM productos_cafeteria

                WHERE id = %s

            """, (
                producto_id,
            ))

        else:

            c.execute("""

                DELETE

                FROM productos_cafeteria

                WHERE id = ?

            """, (
                producto_id,
            ))

        conn.commit()

# ==========================================
# INVENTARIO ACTUAL
# ==========================================
def obtener_inventario_actual_db():

    with conectar() as conn:

        c = conn.cursor()

        c.execute("""

            SELECT

                nombre,
                inventario,
                stock_minimo

            FROM productos_cafeteria

            WHERE estado = 'Activo'

            ORDER BY nombre

        """)

        return c.fetchall()


# ==========================================
# PRODUCTOS VENDIDOS HOY
# ==========================================
def obtener_productos_vendidos_hoy_db():

    with conectar() as conn:

        c = conn.cursor()

        if POSTGRES:

            c.execute("""

                SELECT

                    producto,

                    SUM(cantidad) AS cantidad

                FROM ventas_cafeteria

                WHERE DATE(fecha) = CURRENT_DATE

                GROUP BY producto

                ORDER BY cantidad DESC

            """)

        else:

            c.execute("""

                SELECT

                    producto,

                    SUM(cantidad) AS cantidad

                FROM ventas_cafeteria

                WHERE DATE(fecha)=DATE('now','localtime')

                GROUP BY producto

                ORDER BY cantidad DESC

            """)

        return c.fetchall()

# ==========================================
# REGISTRAR VENTA
# ==========================================
def registrar_venta_cafeteria_db(
    fecha,
    producto_id,
    producto,
    cantidad,
    valor_unitario,
    total,
    placa,
    usuario
):

    with conectar() as conn:

        c = conn.cursor()

        if POSTGRES:

            c.execute("""

                INSERT INTO ventas_cafeteria(

                    fecha,
                    producto_id,
                    producto,
                    cantidad,
                    valor_unitario,
                    total,
                    placa,
                    usuario

                )

                VALUES(

                    %s,%s,%s,%s,%s,%s,%s,%s

                )

            """, (

                fecha,
                producto_id,
                producto,
                cantidad,
                valor_unitario,
                total,
                placa,
                usuario

            ))

            c.execute("""

                UPDATE productos_cafeteria

                SET inventario = inventario - %s

                WHERE id = %s

            """, (

                cantidad,
                producto_id

            ))

        else:

            c.execute("""

                INSERT INTO ventas_cafeteria(

                    fecha,
                    producto_id,
                    producto,
                    cantidad,
                    valor_unitario,
                    total,
                    placa,
                    usuario

                )

                VALUES(?,?,?,?,?,?,?,?)

            """, (

                fecha,
                producto_id,
                producto,
                cantidad,
                valor_unitario,
                total,
                placa,
                usuario

            ))

            c.execute("""

                UPDATE productos_cafeteria

                SET inventario = inventario - ?

                WHERE id = ?

            """, (

                cantidad,
                producto_id

            ))

        conn.commit()
    
# ==========================================
# VENTAS HOY
# ==========================================
def obtener_ventas_hoy_db():

    with conectar() as conn:

        c = conn.cursor()

        if POSTGRES:

            c.execute("""

                SELECT
                    producto,
                    SUM(cantidad) as cantidad

                FROM ventas_cafeteria

                WHERE DATE(fecha) = CURRENT_DATE

                GROUP BY producto

                ORDER BY cantidad DESC

            """)

        else:

            c.execute("""

                SELECT
                    producto,
                    SUM(cantidad) as cantidad

                FROM ventas_cafeteria

                WHERE DATE(fecha) = DATE('now','localtime')

                GROUP BY producto

                ORDER BY cantidad DESC

            """)

        return c.fetchall()
    
# ==========================================
# TOTAL VENTAS HOY
# ==========================================
def obtener_total_ventas_hoy_db():

    with conectar() as conn:

        c = conn.cursor()

        if POSTGRES:

            c.execute("""

                SELECT
                    COALESCE(SUM(total),0)

                FROM ventas_cafeteria

                WHERE DATE(fecha)=CURRENT_DATE

            """)

        else:

            c.execute("""

                SELECT
                    COALESCE(SUM(total),0)

                FROM ventas_cafeteria

                WHERE DATE(fecha)=DATE('now','localtime')

            """)

        resultado = c.fetchone()

        return (
            resultado[0]
            if not isinstance(resultado, dict)
            else list(resultado.values())[0]
        )
    
# ==========================================
# ULTIMAS VENTAS
# ==========================================
def obtener_ultimas_ventas_cafeteria_db():

    with conectar() as conn:

        c = conn.cursor()

        c.execute("""

            SELECT *

            FROM ventas_cafeteria

            ORDER BY id DESC

            LIMIT 20

        """)

        return c.fetchall()