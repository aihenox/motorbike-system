import os
import sqlite3

from contextlib import contextmanager

import psycopg2

from flask import current_app

from psycopg2.extras import (
    RealDictCursor
)


# ==========================================
# CONEXIÓN DATABASE
# ==========================================
@contextmanager
def conectar():

    database_url = os.getenv(
        "DATABASE_URL"
    )

    if database_url:

        conn = conectar_postgres(
            database_url
        )

    else:

        conn = conectar_sqlite()

    try:

        with conn:

            yield conn

    finally:

        conn.close()


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
