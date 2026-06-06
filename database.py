import os

from app.repositories.connection import conectar

from app.services.auth_service import (
    crear_admin_default
)


# ==========================================
# CREAR BASE DE DATOS
# ==========================================
def crear_bd():

    with conectar() as conn:

        c = conn.cursor()

        postgres = os.getenv(
            "DATABASE_URL"
        )

        id_type = (
            "SERIAL PRIMARY KEY"
            if postgres
            else "INTEGER PRIMARY KEY AUTOINCREMENT"
        )

        crear_tabla_ingresos(
            c,
            id_type
        )

        crear_tabla_usuarios(
            c,
            id_type
        )

        crear_tabla_lavados(
            c,
            id_type
        )

        crear_tabla_cierres(
            c,
            id_type
        )

        crear_indices(c)

        conn.commit()

    crear_admin_default()


# ==========================================
# INGRESOS
# ==========================================
def crear_tabla_ingresos(
    c,
    id_type
):

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
# USUARIOS
# ==========================================
def crear_tabla_usuarios(
    c,
    id_type
):

    c.execute(f"""

        CREATE TABLE IF NOT EXISTS usuarios(

            id {id_type},

            usuario TEXT UNIQUE,

            password TEXT,

            rol TEXT

        )

    """)


# ==========================================
# LAVADOS
# ==========================================
def crear_tabla_lavados(
    c,
    id_type
):

    c.execute(f"""

        CREATE TABLE IF NOT EXISTS lavados(

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
# CIERRES
# ==========================================
def crear_tabla_cierres(
    c,
    id_type
):

    c.execute(f"""

        CREATE TABLE IF NOT EXISTS cierres_caja(

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
# ÍNDICES
# ==========================================
def crear_indices(c):

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