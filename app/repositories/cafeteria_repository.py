import os

from datetime import datetime

from zoneinfo import ZoneInfo

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

    venta_id,

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
                    venta_id,
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

                    %s,%s,%s,%s,%s,%s,%s,%s,%s

                )

            """, (
                venta_id,
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
                    venta_id,
                    fecha,
                    producto_id,
                    producto,
                    cantidad,
                    valor_unitario,
                    total,
                    placa,
                    usuario

                )

                VALUES(?,?,?,?,?,?,?,?,?)

            """, (
                venta_id,
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

# ==========================================
# BUSCAR PRODUCTO POR NOMBRE
# ==========================================
def buscar_producto_por_nombre_db(
    nombre
):

    with conectar() as conn:

        c = conn.cursor()

        if POSTGRES:

            c.execute("""

                SELECT *

                FROM productos_cafeteria

                WHERE UPPER(nombre) = UPPER(%s)

            """, (
                nombre,
            ))

        else:

            c.execute("""

                SELECT *

                FROM productos_cafeteria

                WHERE UPPER(nombre) = UPPER(?)

            """, (
                nombre,
            ))

        return c.fetchone()
    
# ==========================================
# OBTENER SIGUIENTE CONSECUTIVO DEL DIA
# ==========================================
def obtener_consecutivo_venta_dia_db():

    with conectar() as conn:

        c = conn.cursor()

        hoy = datetime.now(
            ZoneInfo(
                "America/Bogota"
            )
        ).strftime("%Y-%m-%d")

        operador = (
            "%s"
            if POSTGRES
            else "?"
        )

        c.execute(f"""

            SELECT COUNT(*)

            FROM ventas_cafeteria

            WHERE fecha LIKE {operador}
            AND placa LIKE {operador}

        """, (

            f"{hoy}%",

            "VENTA #%"

        ))

        fila = c.fetchone()

        if POSTGRES:

            cantidad = list(
                fila.values()
            )[0]

        else:

            cantidad = fila[0]

        return cantidad + 1

# ==========================================
# RESUMEN VENTAS DEL DIA
# ==========================================
def obtener_resumen_ventas_hoy_db():

    with conectar() as conn:

        c = conn.cursor()

        if POSTGRES:

            c.execute("""

                SELECT

                    placa,

                    MIN(fecha) as fecha,

                    SUM(total) as total

                FROM ventas_cafeteria

                WHERE DATE(fecha) = CURRENT_DATE

                GROUP BY placa

                ORDER BY MIN(fecha) DESC

            """)

        else:

            c.execute("""

                SELECT

                    placa,

                    MIN(fecha) as fecha,

                    SUM(total) as total

                FROM ventas_cafeteria

                WHERE DATE(fecha)=DATE('now','localtime')

                GROUP BY placa

                ORDER BY MIN(fecha) DESC

            """)

        rows = c.fetchall()

        resultado = []

        for row in rows:

            if POSTGRES:

                fecha = row["fecha"]

                if isinstance(
                    fecha,
                    str
                ):

                    try:

                        fecha = datetime.fromisoformat(
                            fecha
                        )

                    except Exception:

                        fecha = None

                resultado.append({

                    "placa": row["placa"],

                    "fecha": (

                        fecha.strftime(
                            "%I:%M %p"
                        )

                        if fecha

                        else "--:--"

                    ),

                    "total": row["total"] or 0

                })

            else:

                fecha = row[1]

                resultado.append({

                    "placa": row[0],

                    "fecha": datetime.strptime(

                        str(fecha),

                        "%Y-%m-%d %H:%M:%S"

                    ).strftime(

                        "%I:%M %p"

                    ),

                    "total": row[2]

                })

        return resultado

# ==========================================
# HISTORIAL VENTAS CAFETERIA
# ==========================================
def obtener_historial_ventas_cafeteria_db():

    with conectar() as conn:

        c = conn.cursor()

        if POSTGRES:

            c.execute("""

            SELECT

                venta_id,

                placa,

                MIN(fecha) AS fecha,

                COUNT(*) AS productos,

                SUM(total) AS total,

                usuario

            FROM ventas_cafeteria

            GROUP BY

                venta_id,
                placa,
                usuario

            ORDER BY MIN(fecha) DESC
            LIMIT 10
        """)

        else:

            c.execute("""

                SELECT

                    venta_id,

                    placa,

                    MIN(fecha) AS fecha,

                    COUNT(*) AS productos,

                    SUM(total) AS total,

                    usuario

                FROM ventas_cafeteria

                GROUP BY

                    venta_id,
                    placa,
                    usuario

                ORDER BY MIN(fecha) DESC
                LIMIT 10      
                

            """)

        return c.fetchall()
    
# ==========================================
# DETALLE VENTA CAFETERIA
# ==========================================
def obtener_detalle_venta_cafeteria_db(
    venta_id
):

    with conectar() as conn:

        c = conn.cursor()

        if POSTGRES:

            c.execute("""

                SELECT

                    producto,

                    cantidad,

                    valor_unitario,

                    total

                FROM ventas_cafeteria

                WHERE venta_id = %s

                ORDER BY id

            """, (

                venta_id,

            ))

        else:

            c.execute("""

                SELECT

                    producto,

                    cantidad,

                    valor_unitario,

                    total

                FROM ventas_cafeteria

                WHERE venta_id = ?

                ORDER BY id

            """, (

                venta_id,

            ))
        return c.fetchall()
    
# ==========================================
# HISTORIAL POR FECHAS
# ==========================================
def obtener_historial_cafeteria_fechas_db(

    fecha_inicio,

    fecha_fin

):

    with conectar() as conn:

        c = conn.cursor()

        if POSTGRES:

            c.execute("""

                SELECT

                    venta_id,

                    placa,

                    MIN(fecha) AS fecha,

                    COUNT(*) AS productos,

                    SUM(total) AS total,

                    usuario

                FROM ventas_cafeteria

                WHERE DATE(fecha)
                BETWEEN %s AND %s

                GROUP BY

                    venta_id,
                    placa,
                    usuario

                ORDER BY MIN(fecha) DESC

            """, (

                fecha_inicio,

                fecha_fin

            ))

        else:

            c.execute("""

                SELECT

                    venta_id,

                    placa,

                    MIN(fecha) AS fecha,

                    COUNT(*) AS productos,

                    SUM(total) AS total,

                    usuario

                FROM ventas_cafeteria

                WHERE DATE(fecha)
                BETWEEN ? AND ?

                GROUP BY

                    venta_id,
                    placa,
                    usuario

                ORDER BY MIN(fecha) DESC

            """, (

                fecha_inicio,

                fecha_fin

            ))

        return c.fetchall()