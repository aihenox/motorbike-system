import os
import sqlite3

import psycopg2

from flask import current_app

from psycopg2.extras import (
    RealDictCursor
)


# ==========================================
# CONEXIÓN DATABASE
# ==========================================
def conectar():

    database_url = os.getenv(
        "DATABASE_URL"
    )

    if database_url:

        return conectar_postgres(
            database_url
        )

    return conectar_sqlite()


# ==========================================
# POSTGRESQL
# ==========================================
def conectar_postgres(
    database_url
):

    return psycopg2.connect(
        database_url,
        cursor_factory=RealDictCursor
    )


# ==========================================
# SQLITE
# ==========================================
def conectar_sqlite():

    db_path = current_app.config.get(
        "DATABASE_PATH",
        "instance/parqueadero.db"
    )

    os.makedirs(
        os.path.dirname(db_path),
        exist_ok=True
    )

    conn = sqlite3.connect(
        db_path
    )

    conn.row_factory = sqlite3.Row

    return conn