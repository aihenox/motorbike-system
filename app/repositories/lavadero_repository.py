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
            
            fecha_iso = datetime.strptime(

                fecha,

                "%Y-%m-%d"

            ).strftime("%Y-%m-%d")

            valores.append(
                f"{fecha_iso}%"
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

        hoy = datetime.now(
            ZoneInfo(
                "America/Bogota"
        )
        ).strftime(
            "%Y-%m-%d"
        )

        operador = "%s" if POSTGRES else "?"

        c.execute(f"""

            SELECT

                COUNT(
                    CASE
                        WHEN vehiculo = 'Moto'
                        THEN 1
                    END
                ) as motos,

                COUNT(
                    CASE
                        WHEN vehiculo = 'Carro'
                        THEN 1
                    END
                ) as carros,

                COALESCE(
                    SUM(valor),
                    0
                ) as total

            FROM lavados

            WHERE fecha LIKE {operador}

        """, (
            f"{hoy}%",
        ))

        row = c.fetchone()

        if POSTGRES:

            motos = row["motos"]

            carros = row["carros"]

            total = row["total"]

        else:

            motos = row[0]

            carros = row[1]

            total = row[2]

        return {

            "lavados_motos":
                motos,

            "lavados_carros":
                carros,

            "total_lavados":
                motos + carros,

            "dinero_generado":
                total
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

        hoy = datetime.now(
            ZoneInfo(
                "America/Bogota"
        )
        ).strftime(
            "%Y-%m-%d"
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

            if POSTGRES:

                resultado.append({

                    "responsable":
                        row["responsable"],

                    "cantidad":
                        row["cantidad"],

                    "total":
                        row["total"]
                })

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