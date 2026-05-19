from app.repositories.connection import conectar


# ==========================================
# LISTAR HISTORIAL LAVADERO
# ==========================================
def obtener_historial_lavadero_db(

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

        # ==========================================
        # FILTRO PLACA
        # ==========================================
        if placa:

            query += """

                AND placa LIKE ?

            """

            parametros.append(
                f"%{placa}%"
            )

        # ==========================================
        # FILTRO RESPONSABLE
        # ==========================================
        if responsable:

            query += """

                AND responsable LIKE ?

            """

            parametros.append(
                f"%{responsable}%"
            )

        # ==========================================
        # FILTRO FECHA
        # ==========================================
        if fecha:

            fecha_formato = "/".join(
                fecha.split("-")[::-1]
            )

            query += """

                AND fecha LIKE ?

            """

            parametros.append(
                f"{fecha_formato}%"
            )

        # ==========================================
        # ORDEN
        # ==========================================
        query += """

            ORDER BY id DESC

        """

        c.execute(
            query,
            parametros
        )

        return c.fetchall()


# ==========================================
# TOTAL LAVADERO
# ==========================================
def obtener_total_lavadero_db(

    placa="",

    fecha="",

    responsable=""
):

    with conectar() as conn:

        c = conn.cursor()

        query = """

            SELECT COALESCE(
                SUM(valor),
                0
            )

            FROM lavados

            WHERE 1=1

        """

        parametros = []

        # PLACA
        if placa:

            query += """

                AND placa LIKE ?

            """

            parametros.append(
                f"%{placa}%"
            )

        # RESPONSABLE
        if responsable:

            query += """

                AND responsable LIKE ?

            """

            parametros.append(
                f"%{responsable}%"
            )

        # FECHA
        if fecha:

            fecha_formato = "/".join(
                fecha.split("-")[::-1]
            )

            query += """

                AND fecha LIKE ?

            """

            parametros.append(
                f"{fecha_formato}%"
            )

        c.execute(
            query,
            parametros
        )

        total = c.fetchone()[0]

        return total or 0