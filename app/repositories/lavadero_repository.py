import os

from datetime import datetime

from app.repositories.connection import conectar


# ==========================================
# MOTOR DATABASE
# ==========================================
POSTGRES = os.getenv(
    "DATABASE_URL"
)


# ==========================================
# HELPER VALOR
# ==========================================
def obtener_valor(row):

    if POSTGRES:

        return list(row.values())[0]

    return row[0]


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

        # ==========================================
        # POSTGRESQL
        # ==========================================
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

                VALUES (

                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s

                )

            """, (

                placa.upper(),

                vehiculo,

                tipo_lavado,

                valor,

                responsable,

                fecha
            ))

        # ==========================================
        # SQLITE
        # ==========================================
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

                VALUES (

                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?

                )

            """, (

                placa.upper(),

                vehiculo,

                tipo_lavado,

                valor,

                responsable,

                fecha
            ))

        conn.commit()


# ==========================================
# OBTENER LAVADOS
# ==========================================
def obtener_lavados_db():

    with conectar() as conn:

        c = conn.cursor()

        c.execute("""

            SELECT *

            FROM lavados

            ORDER BY id DESC

        """)

        return c.fetchall()


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

        condiciones = []

        valores = []

        operador = "%s" if POSTGRES else "?"

        # ==========================================
        # FILTRO PLACA
        # ==========================================
        if placa:

            condiciones.append(
                f"placa LIKE {operador}"
            )

            valores.append(
                f"%{placa.upper()}%"
            )

        # ==========================================
        # FILTRO FECHA
        # ==========================================
        if fecha:

            condiciones.append(
                f"fecha LIKE {operador}"
            )

            valores.append(
                f"{fecha}%"
            )

        # ==========================================
        # FILTRO RESPONSABLE
        # ==========================================
        if responsable:

            condiciones.append(
                f"responsable = {operador}"
            )

            valores.append(
                responsable
            )

        query = """

            SELECT *

            FROM lavados

        """

        if condiciones:

            query += " WHERE " + " AND ".join(
                condiciones
            )

        query += """

            ORDER BY id DESC

        """

        c.execute(
            query,
            tuple(valores)
        )

        return c.fetchall()


# ==========================================
# METRICAS LAVADERO
# ==========================================
def obtener_metricas_lavadero_db():

    with conectar() as conn:

        c = conn.cursor()

        hoy = datetime.now().strftime(
            "%d/%m/%Y"
        )

        operador = "%s" if POSTGRES else "?"

        # ==========================================
        # MOTOS HOY
        # ==========================================
        c.execute(f"""

            SELECT COUNT(*)

            FROM lavados

            WHERE vehiculo = 'Moto'

            AND fecha LIKE {operador}

        """, (
            f"{hoy}%",
        ))

        lavados_motos = obtener_valor(
            c.fetchone()
        )

        # ==========================================
        # CARROS HOY
        # ==========================================
        c.execute(f"""

            SELECT COUNT(*)

            FROM lavados

            WHERE vehiculo = 'Carro'

            AND fecha LIKE {operador}

        """, (
            f"{hoy}%",
        ))

        lavados_carros = obtener_valor(
            c.fetchone()
        )

        # ==========================================
        # TOTAL GENERADO HOY
        # ==========================================
        c.execute(f"""

            SELECT COALESCE(
                SUM(valor),
                0
            )

            FROM lavados

            WHERE fecha LIKE {operador}

        """, (
            f"{hoy}%",
        ))

        dinero_generado = obtener_valor(
            c.fetchone()
        )

        return {

            "lavados_motos":
                lavados_motos,

            "lavados_carros":
                lavados_carros,

            "total_lavados":
                lavados_motos
                +
                lavados_carros,

            "dinero_generado":
                dinero_generado
        }


# ==========================================
# ULTIMOS LAVADOS
# ==========================================
def obtener_ultimos_lavados_db():

    with conectar() as conn:

        c = conn.cursor()

        c.execute("""

            SELECT *

            FROM lavados

            ORDER BY id DESC

            LIMIT 10

        """)

        return c.fetchall()


# ==========================================
# ESTADISTICAS RESPONSABLES
# ==========================================
def obtener_estadisticas_responsables_db():

    with conectar() as conn:

        c = conn.cursor()

        hoy = datetime.now().strftime(
            "%d/%m/%Y"
        )

        operador = "%s" if POSTGRES else "?"

        c.execute(f"""

            SELECT

                responsable,

                COUNT(*) as cantidad,

                COALESCE(
                    SUM(valor),
                    0
                ) as total

            FROM lavados

            WHERE fecha LIKE {operador}

            GROUP BY responsable

            ORDER BY total DESC

        """, (
            f"{hoy}%",
        ))

        rows = c.fetchall()

        resultado = []

        for row in rows:

            # ==========================================
            # POSTGRESQL
            # ==========================================
            if POSTGRES:

                resultado.append({

                    "responsable":
                        row["responsable"],

                    "cantidad":
                        row["cantidad"],

                    "total":
                        row["total"]
                })

            # ==========================================
            # SQLITE
            # ==========================================
            else:

                resultado.append({

                    "responsable":
                        row[0],

                    "cantidad":
                        row[1],

                    "total":
                        row[2]
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

        operador = "%s" if POSTGRES else "?"

        c.execute(f"""

            SELECT *

            FROM lavados

            WHERE id = {operador}

        """, (
            lavado_id,
        ))

        return c.fetchone()


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

        operador = "%s" if POSTGRES else "?"

        c.execute(f"""

            UPDATE lavados

            SET

                placa = {operador},
                vehiculo = {operador},
                tipo_lavado = {operador},
                valor = {operador},
                responsable = {operador}

            WHERE id = {operador}

        """, (

            placa.upper(),

            vehiculo,

            tipo_lavado,

            valor,

            responsable,

            lavado_id
        ))

        conn.commit()