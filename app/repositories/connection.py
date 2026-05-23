import os
import sqlite3
import psycopg2

from flask import current_app
from psycopg2.extras import RealDictCursor


# ==========================================
# CONEXIÓN DATABASE
# ==========================================
def conectar():

    database_url = os.getenv(
        "DATABASE_URL"
    )

    # ==========================================
    # POSTGRESQL ONLINE
    # ==========================================
    if database_url:

        conn = psycopg2.connect(
            database_url,
            cursor_factory=RealDictCursor
        )

        return conn

    # ==========================================
    # SQLITE LOCAL
    # ==========================================
    db_path = current_app.config.get(
        "DATABASE_PATH",
        "instance/parqueadero.db"
    )

    os.makedirs(
        os.path.dirname(db_path),
        exist_ok=True
    )

    conn = sqlite3.connect(db_path)

    conn.row_factory = sqlite3.Row

    return conn