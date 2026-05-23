import os

from app.repositories.connection import conectar


# ==========================================
# MOTOR DATABASE
# ==========================================
POSTGRES = os.getenv(
    "DATABASE_URL"
)


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

        operador = "%s" if POSTGRES else "?"

        query = """

            SELECT
                id,
                placa,
                vehiculo,
                tipo_lavado,
                valor,
                responsable,
                fecha

            FROM lavados

            WHERE 1=1

        """

        parametros = []

        # ==========================================
        # PLACA
        # ==========================================
        if placa:

            query += f"""

                AND placa LIKE {operador}

            """

            parametros.append(
                f"%{placa}%"
            )

        # ==========================================
        # RESPONSABLE
        # ==========================================
        if responsable:

            query += f"""

                AND responsable LIKE {operador}

            """

            parametros.append(
                f"%{responsable}%"
            )

        # ==========================================
        # FECHA
        # ==========================================
        if fecha:

            query += f"""

                AND fecha LIKE {operador}

            """

            parametros.append(
                f"{fecha}%"
            )

        query += """

            ORDER BY id DESC

        """

        c.execute(
            query,
            tuple(parametros)
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

        operador = "%s" if POSTGRES else "?"

        query = """

            SELECT

                COALESCE(
                    SUM(valor),
                    0
                ) AS total

            FROM lavados

            WHERE 1=1

        """

        parametros = []

        # ==========================================
        # PLACA
        # ==========================================
        if placa:

            query += f"""

                AND placa LIKE {operador}

            """

            parametros.append(
                f"%{placa}%"
            )

        # ==========================================
        # RESPONSABLE
        # ==========================================
        if responsable:

            query += f"""

                AND responsable LIKE {operador}

            """

            parametros.append(
                f"%{responsable}%"
            )

        # ==========================================
        # FECHA
        # ==========================================
        if fecha:

            query += f"""

                AND fecha LIKE {operador}

            """

            parametros.append(
                f"{fecha}%"
            )

        c.execute(
            query,
            tuple(parametros)
        )

        row = c.fetchone()

        # ==========================================
        # POSTGRESQL
        # ==========================================
        if POSTGRES:

            return row["total"] or 0

        # ==========================================
        # SQLITE
        # ==========================================
        return row[0] or 0
