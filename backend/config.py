"""Configuración central de la aplicación.

Lee las variables de entorno y expone una instancia única de Config.

En Render (producción) la conexión MySQL se define con:
  MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE
  (también se acepta DATABASE_URL con formato mysql://usuario:pass@host:puerto/bd)

Si no hay configuración MySQL, la app usa SQLite (solo para desarrollo local).
"""

import os
from pathlib import Path
from urllib.parse import urlparse

BASE_DIR = Path(__file__).resolve().parent


def _a_true(valor):
    return str(valor or "").strip().lower() in ("1", "true", "yes", "on")


class Config:
    def __init__(self):
        self.port = int(os.environ.get("PORT", os.environ.get("APP_PORT", "8000")))
        self.secret_key = os.environ.get(
            "SECRET_KEY", "clave-insegura-cambiar-en-produccion"
        )
        self.debug = _a_true(os.environ.get("FLASK_DEBUG", "false"))

        # --- Detección del tipo de base de datos ---
        url = (os.environ.get("DATABASE_URL") or "").strip()

        if url.startswith("mysql://") or url.startswith("mariadb://"):
            self.db_type = "mysql"
            parsed = urlparse(url)
            self.mysql_host = parsed.hostname or "localhost"
            self.mysql_port = parsed.port or 3306
            self.mysql_user = parsed.username or "root"
            self.mysql_password = parsed.password or ""
            self.mysql_database = (parsed.path or "").lstrip("/") or "finanzas_personales"
        elif os.environ.get("MYSQL_HOST"):
            self.db_type = "mysql"
            self.mysql_host = os.environ.get("MYSQL_HOST", "localhost")
            self.mysql_port = int(os.environ.get("MYSQL_PORT", "3306") or 3306)
            self.mysql_user = os.environ.get("MYSQL_USER", "root")
            self.mysql_password = os.environ.get("MYSQL_PASSWORD", "")
            self.mysql_database = os.environ.get("MYSQL_DATABASE", "finanzas_personales")
        else:
            self.db_type = "sqlite"
            self.sqlite_path = Path(
                os.environ.get("SQLITE_PATH", str(BASE_DIR / "finanzas_local.db"))
            )

        # Algunos proveedores de MySQL en la nube requieren SSL/TLS.
        self.mysql_ssl = _a_true(os.environ.get("MYSQL_SSL", "false"))

        # Carga el demo (usuario + categorías + movimientos) si la BD está vacía.
        self.seed_demo = _a_true(os.environ.get("SEED_DEMO", "true"))

        # Hosts rotatorios (-) usados por CORS.
        self.cors_origins = os.environ.get(
            "CORS_ORIGINS", "*"
        )


# Instancia única accesible desde cualquier módulo.
config = Config()