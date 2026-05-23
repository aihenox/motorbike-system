import os

from app.repositories.connection import conectar

from app.services.auth_service import (
    crear_admin_default
)


# ==========================================
# CREAR BASE DATOS
# ==========================================
def crear_bd():

    with conectar() as conn:

        c = conn.cursor()

        # ==========================================
        # DETECTAR POSTGRESQL
        # ==========================================
        postgres = os.getenv(
            "DATABASE_URL"
        )

        # ==========================================
        # AUTO INCREMENT
        # ==========================================
        if postgres:

            id_type = "SERIAL PRIMARY KEY"

        else:

            id_type = (
                "INTEGER PRIMARY KEY AUTOINCREMENT"
            )

        # ==========================================
        # TABLA INGRESOS
        # ==========================================
        c.execute(f"""

            CREATE TABLE IF NOT EXISTS ingresos(

                id {id_type},

                placa TEXT NOT NULL,

                tipo TEXT NOT NULL,

                hora_ingreso TEXT NOT NULL,

                hora_salida TEXT,

                valor INTEGER,

                estado TEXT NOT NULL
            )

        """)

        # ==========================================
        # TABLA USUARIOS
        # ==========================================
        c.execute(f"""

            CREATE TABLE IF NOT EXISTS usuarios(

                id {id_type},

                usuario TEXT UNIQUE,

                password TEXT,

                rol TEXT
            )

        """)

        # ==========================================
        # TABLA LAVADOS
        # ==========================================
        c.execute(f"""

            CREATE TABLE IF NOT EXISTS lavados (

                id {id_type},

                placa TEXT NOT NULL,

                vehiculo TEXT NOT NULL,

                tipo_lavado TEXT NOT NULL,

                valor INTEGER NOT NULL,

                responsable TEXT NOT NULL,

                fecha TEXT NOT NULL
            )

        """)

        # ==========================================
        # TABLA CIERRES
        # ==========================================
        c.execute(f"""

            CREATE TABLE IF NOT EXISTS cierres_caja (

                id {id_type},

                fecha TEXT NOT NULL,

                total_parqueadero INTEGER NOT NULL,

                total_lavadero INTEGER NOT NULL,

                total_general INTEGER NOT NULL,

                observaciones TEXT,

                usuario TEXT NOT NULL,

                hora_cierre TEXT NOT NULL
            )

        """)

        # ==========================================
        # INDEX INGRESOS
        # ==========================================
        c.execute("""

            CREATE INDEX IF NOT EXISTS idx_placa
            ON ingresos(placa)

        """)

        c.execute("""

            CREATE INDEX IF NOT EXISTS idx_estado
            ON ingresos(estado)

        """)

        c.execute("""

            CREATE INDEX IF NOT EXISTS idx_ingresos_estado_placa
            ON ingresos(estado, placa)

        """)

        c.execute("""

            CREATE INDEX IF NOT EXISTS idx_ingresos_estado_hora
            ON ingresos(estado, hora_ingreso)

        """)

        c.execute("""

            CREATE INDEX IF NOT EXISTS idx_hora_ingreso
            ON ingresos(hora_ingreso)

        """)

        # ==========================================
        # INDEX LAVADOS
        # ==========================================
        c.execute("""

            CREATE INDEX IF NOT EXISTS idx_lavados_fecha
            ON lavados(fecha)

        """)

        c.execute("""

            CREATE INDEX IF NOT EXISTS idx_lavados_responsable
            ON lavados(responsable)

        """)

        c.execute("""

            CREATE INDEX IF NOT EXISTS idx_lavados_placa
            ON lavados(placa)

        """)

        conn.commit()

    # ==========================================
    # CREAR ADMIN
    # ==========================================
    crear_admin_default()
