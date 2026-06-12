import os

from app.repositories.connection import conectar

from app.utils.date_utils import formatear_fecha

from datetime import datetime

from zoneinfo import ZoneInfo


# ==========================================
# MOTOR DATABASE
# ==========================================
POSTGRES = os.getenv(
    "DATABASE_URL"
)


# ==========================================
# HELPER FETCH
# ==========================================
def obtener_valor(row):

    if not row:
        return 0

    if POSTGRES:
        return list(row.values())[0] or 0

    return row[0] or 0


# ==========================================
# MÉTRICAS DASHBOARD
# ==========================================
def obtener_metricas_dashboard_db():

    with conectar() as conn:

        c = conn.cursor()

        hoy = datetime.now(
            ZoneInfo("America/Bogota")
        ).strftime("%Y-%m-%d")

        operador = "%s" if POSTGRES else "?"

        # ==========================================
        # VEHÍCULOS ACTIVOS
        # ==========================================
        c.execute("""

            SELECT COUNT(*)

            FROM ingresos

            WHERE estado = 'Dentro'

        """)

        total_activos = obtener_valor(
            c.fetchone()
        )

        # ==========================================
        # MOTOS FUERA HOY
        # ==========================================
        c.execute(f"""

            SELECT COUNT(*)

            FROM ingresos

            WHERE estado = 'Fuera'
            AND tipo = 'Moto'
            AND hora_salida LIKE {operador}

        """, (
            f"{hoy}%",
        ))

        motos_fuera = obtener_valor(
            c.fetchone()
        )

        # ==========================================
        # CARROS FUERA HOY
        # ==========================================
        c.execute(f"""

            SELECT COUNT(*)

            FROM ingresos

            WHERE estado = 'Fuera'
            AND tipo = 'Carro'
            AND hora_salida LIKE {operador}

        """, (
            f"{hoy}%",
        ))

        carros_fuera = obtener_valor(
            c.fetchone()
        )

        # ==========================================
        # TOTAL PARQUEADERO HOY
        # ==========================================
        c.execute(f"""

            SELECT COALESCE(
                SUM(valor),
                0
            )

            FROM ingresos

            WHERE estado = 'Fuera'
            AND hora_salida LIKE {operador}

        """, (
            f"{hoy}%",
        ))

        total_parqueadero = obtener_valor(
            c.fetchone()
        )

        # ==========================================
        # LAVADOS MOTOS HOY
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
        # LAVADOS CARROS HOY
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
        # TOTAL LAVADERO HOY
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

        total_lavadero = obtener_valor(
            c.fetchone()
        )

        # ==========================================
        # TOTAL GENERAL HOY
        # ==========================================
        total_general_hoy = int(
            total_parqueadero or 0
        ) + int(
            total_lavadero or 0
        )

        return {

            "total_activos": total_activos,

            "motos_fuera": motos_fuera,

            "carros_fuera": carros_fuera,

            "total_parqueadero": total_parqueadero,

            "lavados_motos": lavados_motos,

            "lavados_carros": lavados_carros,

            "total_servicios": total_lavadero,

            "total_general_hoy": total_general_hoy
        }

# ==========================================
# ÚLTIMOS INGRESOS
# ==========================================
def obtener_ultimos_ingresos_db(
    limite=10
):

    with conectar() as conn:

        c = conn.cursor()

        query = f"""

            SELECT

                placa,
                tipo,
                hora_ingreso,
                hora_salida,
                estado

            FROM ingresos

            ORDER BY id DESC

            LIMIT {int(limite)}

        """

        c.execute(query)

        rows = c.fetchall()

        resultado = []

        for row in rows:

            if POSTGRES:

                resultado.append({

                    "placa": row["placa"],

                    "tipo": row["tipo"],

                    "hora_ingreso": formatear_fecha(
                        row["hora_ingreso"]
                    ),

                    "hora_salida": formatear_fecha(
                        row["hora_salida"]
                    ),

                    "estado": row["estado"]
                })

            else:

                resultado.append({

                    "placa": row[0],

                    "tipo": row[1],

                    "hora_ingreso": formatear_fecha(
                        row[2]
                    ),

                    "hora_salida": formatear_fecha(
                        row[3]
                    ),

                    "estado": row[4]
                })

        return resultado 
    

# ==========================================
# CONSUMOS DEL DIA POR PLACA
# ==========================================
def obtener_consumos_placas_db():

    with conectar() as conn:

        c = conn.cursor()

        hoy = datetime.now(
            ZoneInfo(
                "America/Bogota"
            )
        ).strftime("%Y-%m-%d")

        consumos = {}

        operador = (
            "%s"
            if POSTGRES
            else "?"
        )

        # ==========================
        # LAVADERO
        # ==========================
        c.execute(f"""

            SELECT

                placa,

                valor

            FROM lavados

            WHERE placa IS NOT NULL
            AND placa <> ''
            AND fecha LIKE {operador}

        """, (
            f"{hoy}%",
        ))

        for row in c.fetchall():

            placa = (
                row["placa"]
                if POSTGRES
                else row[0]
            )

            valor = (
                row["valor"]
                if POSTGRES
                else row[1]
            )

            if placa not in consumos:

                consumos[placa] = {

                    "placa": placa,

                    "total": 0

                }

            consumos[placa]["total"] += (
                valor or 0
            )

        # ==========================
        # CAFETERIA
        # ==========================
        c.execute(f"""

            SELECT

                placa,

                total

            FROM ventas_cafeteria

            WHERE placa IS NOT NULL
            AND placa <> ''
            AND fecha LIKE {operador}

        """, (
            f"{hoy}%",
        ))

        rows = c.fetchall()

        print(
            "VENTAS ENCONTRADAS:",
            rows
        )

        for row in rows:

            placa = (
                row["placa"]
                if POSTGRES
                else row[0]
            )

            total = (
                row["total"]
                if POSTGRES
                else row[1]
            )

            if placa not in consumos:

                consumos[placa] = {

                    "placa": placa,

                    "total": 0

                }

            consumos[placa]["total"] += (
                total or 0
            )

        return sorted(

            consumos.values(),

            key=lambda x: x["total"],

            reverse=True

        )
    
# ==========================================
# DETALLE CONSUMOS DEL DIA POR PLACA
# ==========================================
def obtener_detalle_consumos_placa_db(
    placa
):

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

        resultado = {

            "placa": placa,

            "lavados": [],

            "cafeteria": [],

            "total": 0

        }

        # ==========================
        # LAVADERO
        # ==========================
        c.execute(f"""

            SELECT

                tipo_lavado,

                valor

            FROM lavados

            WHERE placa = {operador}
            AND fecha LIKE {operador}

            ORDER BY id DESC

        """, (

            placa,

            f"{hoy}%"

        ))

        for row in c.fetchall():

            if POSTGRES:

                descripcion = row["tipo_lavado"]

                valor = row["valor"]

            else:

                descripcion = row[0]

                valor = row[1]

            resultado["lavados"].append({

                "descripcion": descripcion,

                "valor": valor

            })

            resultado["total"] += (
                valor or 0
            )

        # ==========================
        # CAFETERIA
        # ==========================
        c.execute(f"""

            SELECT

                producto,

                cantidad,

                total

            FROM ventas_cafeteria

            WHERE placa = {operador}
            AND fecha LIKE {operador}

            ORDER BY id DESC

        """, (

            placa,

            f"{hoy}%"

        ))

        for row in c.fetchall():

            if POSTGRES:

                producto = row["producto"]

                cantidad = row["cantidad"]

                total = row["total"]

            else:

                producto = row[0]

                cantidad = row[1]

                total = row[2]

            resultado["cafeteria"].append({

                "producto": producto,

                "cantidad": cantidad,

                "total": total

            })

            resultado["total"] += (
                total or 0
            )

        return resultado