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

        crear_tabla_tarifas(
            c,
            id_type
        )

        crear_tabla_mensualidades(
            c,
            id_type
        )

        actualizar_tabla_ingresos(c)

        crear_indices(c)

        insertar_tarifas_default(c)

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
# CONFIGURACION TARIFAS
# ==========================================
def crear_tabla_tarifas(
    c,
    id_type
):

    c.execute(f"""

        CREATE TABLE IF NOT EXISTS configuracion_tarifas(

            id {id_type},

            hora_moto INTEGER,

            hora_carro INTEGER,

            fraccion_moto INTEGER,

            fraccion_carro INTEGER,

            dia_moto INTEGER,

            dia_carro INTEGER,

            noche_moto INTEGER,

            noche_carro INTEGER,

            mensualidad_moto INTEGER,

            mensualidad_carro INTEGER,

            minutos_gracia INTEGER

        )

    """)


# ==========================================
# MENSUALIDADES
# ==========================================
def crear_tabla_mensualidades(
    c,
    id_type
):

    c.execute(f"""

        CREATE TABLE IF NOT EXISTS mensualidades(

            id {id_type},

            placa TEXT NOT NULL,

            tipo TEXT NOT NULL,

            propietario TEXT,

            telefono TEXT,

            fecha_inicio TEXT,

            fecha_fin TEXT,

            estado TEXT NOT NULL

        )

    """)


# ==========================================
# MIGRACION INGRESOS
# ==========================================
def actualizar_tabla_ingresos(c):

    postgres = os.getenv(
        "DATABASE_URL"
    )

    columnas = [

        (
            "modalidad",
            "TEXT DEFAULT 'Hora'"
        ),

        (
            "puesto_casco",
            "INTEGER"
        ),

        (
            "cantidad_cascos",
            "INTEGER DEFAULT 0"
        )
    ]

    for nombre, tipo in columnas:

        if postgres:

            c.execute("""

                SELECT column_name

                FROM information_schema.columns

                WHERE table_name = 'ingresos'
                AND column_name = %s

            """, (
                nombre,
            ))

            existe = c.fetchone()

            if not existe:

                c.execute(
                    f"""
                    ALTER TABLE ingresos
                    ADD COLUMN {nombre} {tipo}
                    """
                )

        else:

            try:

                c.execute(
                    f"""
                    ALTER TABLE ingresos
                    ADD COLUMN {nombre} {tipo}
                    """
                )

            except Exception:

                pass


# ==========================================
# TARIFAS POR DEFECTO
# ==========================================
def insertar_tarifas_default(c):

    try:

        c.execute("""
            SELECT COUNT(*)
            FROM configuracion_tarifas
        """)

        resultado = c.fetchone()

        cantidad = (
            resultado[0]
            if not isinstance(
                resultado,
                dict
            )
            else list(
                resultado.values()
            )[0]
        )

        if cantidad == 0:

            c.execute("""

                INSERT INTO configuracion_tarifas(

                    hora_moto,
                    hora_carro,

                    fraccion_moto,
                    fraccion_carro,

                    dia_moto,
                    dia_carro,

                    noche_moto,
                    noche_carro,

                    mensualidad_moto,
                    mensualidad_carro,

                    minutos_gracia

                )

                VALUES (

                    1500,
                    3000,

                    500,
                    1000,

                    10000,
                    20000,

                    5000,
                    10000,

                    50000,
                    100000,

                    10

                )

            """)

    except Exception:

        pass


# ==========================================
# INDICES
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