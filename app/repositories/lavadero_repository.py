import os

from app.repositories.connection import conectar


# ==========================================
# MOTOR DATABASE
# ==========================================
POSTGRES = os.getenv(
    "DATABASE_URL"
)


# ==========================================
# HELPER ROW
# ==========================================
def convertir_row_lavado(row):

    if not row:
        return None

    # PostgreSQL
    if POSTGRES:

        return {

            "id": row["id"],

            "placa": row["placa"],

            "vehiculo": row["vehiculo"],

            "tipo_lavado": row["tipo_lavado"],

            "valor": row["valor"],

            "responsable": row["responsable"],

            "fecha": row["fecha"]
        }

    # SQLite
    return {

        "id": row[0],

        "placa": row[1],

        "vehiculo": row[2],

        "tipo_lavado": row[3],

        "valor": row[4],

        "responsable": row[5],

        "fecha": row[6]
    }


# ==========================================
# HELPER VALOR
# ==========================================
def obtener_valor(row):

    if not row:
        return 0

    if POSTGRES:
        return list(row.values())[0] or 0

    return row[0] or 0


# ==========================================
# REGISTRAR LAVADO
# ==========================================
def registrar_lavado_db(

    placa,
    vehiculo,
    tipo_lavado,
    valor,
    responsable,
    fecha
):

    with conectar() as conn:

        c = conn.cursor()

        if POSTGRES:

            c.execute("""

                INSERT INTO lavados (

                    placa,
                    vehiculo,
                    tipo_lavado,
                    valor,
                    responsable,
                    fecha

                )

                VALUES (%s, %s, %s, %s, %s, %s)

            """, (

                placa,
                vehiculo,
                tipo_lavado,
                valor,
                responsable,
                fecha
            ))

        else:

            c.execute("""

                INSERT INTO lavados (

                    placa,
                    vehiculo,
                    tipo_lavado,
                    valor,
                    responsable,
                    fecha

                )

                VALUES (?, ?, ?, ?, ?, ?)

            """, (

                placa,
                vehiculo,
                tipo_lavado,
                valor,
                responsable,
                fecha
            ))

        conn.commit()


# ==========================================
# OBTENER TODOS LOS LAVADOS
# ==========================================
def obtener_lavados_db():

    with conectar() as conn:

        c = conn.cursor()

        c.execute("""

            SELECT *

            FROM lavados

            ORDER BY id DESC

        """)

        rows = c.fetchall()

        resultado = []

        for row in rows:

            resultado.append(
                convertir_row_lavado(row)
            )

        return resultado


# ==========================================
# HISTORIAL LAVADOS
# ==========================================
def obtener_historial_lavados_db(

    placa="",
    fecha="",
    responsable=""
):

    with conectar() as conn:

        c = conn.cursor()

        query = """

            SELECT *

            FROM lavados

            WHERE 1=1

        """

        parametros = []

        if placa:

            if POSTGRES:

                query += """

                    AND placa LIKE %s

                """

            else:

                query += """

                    AND placa LIKE ?

                """

            parametros.append(
                f"%{placa}%"
            )

        if fecha:

            if POSTGRES:

                query += """

                    AND fecha LIKE %s

                """

            else:

                query += """

                    AND fecha LIKE ?

                """

            parametros.append(
                f"%{fecha}%"
            )

        if responsable:

            if POSTGRES:

                query += """

                    AND responsable = %s

                """

            else:

                query += """

                    AND responsable = ?

                """

            parametros.append(
                responsable
            )

        query += """

            ORDER BY id DESC

        """

        c.execute(
            query,
            tuple(parametros)
        )

        rows = c.fetchall()

        resultado = []

        for row in rows:

            resultado.append(
                convertir_row_lavado(row)
            )

        return resultado


# ==========================================
# MÉTRICAS LAVADERO
# ==========================================
def obtener_metricas_lavadero_db():

    with conectar() as conn:

        c = conn.cursor()

        c.execute("""

            SELECT COUNT(*)

            FROM lavados

            WHERE vehiculo = 'Moto'

        """)

        lavados_motos = obtener_valor(
            c.fetchone()
        )

        c.execute("""

            SELECT COUNT(*)

            FROM lavados

            WHERE vehiculo = 'Carro'

        """)

        lavados_carros = obtener_valor(
            c.fetchone()
        )

        total_lavados = (

            lavados_motos
            +
            lavados_carros
        )

        c.execute("""

            SELECT COALESCE(
                SUM(valor),
                0
            )

            FROM lavados

        """)

        dinero_generado = obtener_valor(
            c.fetchone()
        )

        return {

            "lavados_motos":
                lavados_motos,

            "lavados_carros":
                lavados_carros,

            "total_lavados":
                total_lavados,

            "dinero_generado":
                dinero_generado
        }


# ==========================================
# ÚLTIMOS LAVADOS
# ==========================================
def obtener_ultimos_lavados_db():

    return obtener_lavados_db()[:10]


# ==========================================
# ESTADISTICAS RESPONSABLES
# ==========================================
def obtener_estadisticas_responsables_db():

    with conectar() as conn:

        c = conn.cursor()

        c.execute("""

            SELECT

                responsable,

                COUNT(*) as cantidad,

                COALESCE(
                    SUM(valor),
                    0
                ) as total

            FROM lavados

            GROUP BY responsable

            ORDER BY total DESC

        """)

        rows = c.fetchall()

        resultado = []

        for row in rows:

            # PostgreSQL
            if POSTGRES:

                resultado.append({

                    "responsable": row["responsable"],

                    "cantidad": row["cantidad"],

                    "total": row["total"]
                })

            # SQLite
            else:

                resultado.append({

                    "responsable": row[0],

                    "cantidad": row[1],

                    "total": row[2]
                })

        return resultado


# ==========================================
# OBTENER LAVADO POR ID
# ==========================================
def obtener_lavado_por_id_db(
    lavado_id
):

    with conectar() as conn:

        c = conn.cursor()

        if POSTGRES:

            c.execute("""

                SELECT *

                FROM lavados

                WHERE id = %s

            """, (

                lavado_id,

            ))

        else:

            c.execute("""

                SELECT *

                FROM lavados

                WHERE id = ?

            """, (

                lavado_id,

            ))

        row = c.fetchone()

        return convertir_row_lavado(row)


# ==========================================
# ACTUALIZAR LAVADO
# ==========================================
def actualizar_lavado_db(

    lavado_id,

    placa,

    vehiculo,

    tipo_lavado,

    valor,

    responsable
):

    with conectar() as conn:

        c = conn.cursor()

        if POSTGRES:

            c.execute("""

                UPDATE lavados

                SET

                    placa = %s,

                    vehiculo = %s,

                    tipo_lavado = %s,

                    valor = %s,

                    responsable = %s

                WHERE id = %s

            """, (

                placa,

                vehiculo,

                tipo_lavado,

                valor,

                responsable,

                lavado_id
            ))

        else:

            c.execute("""

                UPDATE lavados

                SET

                    placa = ?,

                    vehiculo = ?,

                    tipo_lavado = ?,

                    valor = ?,

                    responsable = ?

                WHERE id = ?

            """, (

                placa,

                vehiculo,

                tipo_lavado,

                valor,

                responsable,

                lavado_id
            ))

        conn.commit()