"""Aplicación principal - API REST + Frontend estático.

Ejecución local:
    python backend/app.py

Producción (Render):
    gunicorn backend.app:app
"""

import logging
import os
import sys
from pathlib import Path

# Permite ejecutar tanto `python backend/app.py` como `gunicorn backend.app:app`.
if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from flask import Flask, jsonify, render_template, request, send_from_directory
from flask_cors import CORS

from backend.config import config
from backend.modelos import database
from backend.rutas.auth import auth_bp
from backend.rutas.categorias import categorias_bp
from backend.rutas.movimientos import movimientos_bp
from backend.rutas.resumen import resumen_bp
from backend.rutas.analitica import analitica_bp
from backend.rutas.dashboard import dashboard_bp
from backend.rutas.helpers import ErrorControlador, respuesta_error

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("finanzas")

FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"


def crear_app():
    app = Flask(
        __name__,
        template_folder=str(FRONTEND_DIR),
        static_folder=str(FRONTEND_DIR),
        static_url_path="/static",
    )
    app.config["SECRET_KEY"] = config.secret_key
    app.config["JSON_SORT_KEYS"] = False

    # Origen permitido: mismo dominio en Render. Configurable por CORS_ORIGINS.
    orígenes = [o.strip() for o in config.cors_origins.split(",") if o.strip()]
    CORS(
        app,
        resources={
            r"/api/*": {
                "origins": "*" if orígenes == ["*"] else orígenes,
                "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
                "allow_headers": ["Content-Type", "Authorization"],
                "expose_headers": ["Content-Type"],
            }
        },
        supports_credentials=False,
    )

    # Registro de blueprints de la API.
    app.register_blueprint(auth_bp)
    app.register_blueprint(categorias_bp)
    app.register_blueprint(movimientos_bp)
    app.register_blueprint(resumen_bp)
    app.register_blueprint(analitica_bp)
    app.register_blueprint(dashboard_bp)

    # ---------------- Frontend ----------------
    @app.get("/")
    def index():
        return render_template("index.html")

    @app.get("/favicon.ico")
    def favicon():
        return send_from_directory(
            str(FRONTEND_DIR / "img"), "favicon.svg", mimetype="image/svg+xml"
        )

    # ---------------- Salud / verificación ----------------
    @app.get("/api/salud")
    def salud():
        estado_bd = "error"
        try:
            database.db.fetch_one("SELECT 1 AS ok")
            estado_bd = "conectada"
        except Exception as exc:  # noqa: BLE001
            logger.error("Salud de BD: %s", exc)
        return jsonify(
            {
                "ok": True,
                "servicio": "finanzas-personales",
                "base_de_datos": estado_bd,
                "esquema": config.db_type,
            }
        )

    # ---------------- Manejo de errores ----------------
    @app.errorhandler(ErrorControlador)
    def manejar_error_controlado(exc):
        return respuesta_error(exc.mensaje, exc.codigo)

    @app.errorhandler(404)
    def no_encontrado(_exc):
        if request.path.startswith("/api/"):
            return respuesta_error("Recurso no encontrado.", 404)
        return render_template("index.html"), 404

    @app.errorhandler(405)
    def metodo_no_permitido(_exc):
        return respuesta_error("Método no permitido para este recurso.", 405)

    @app.errorhandler(500)
    def error_interno(_exc):
        logger.exception("Error interno del servidor")
        return respuesta_error("Error interno del servidor. Intente nuevamente.", 500)

    return app


app = crear_app()


def inicializar_datos():
    """Prepara esquema y datos demo al arrancar (sin bloquear la API)."""
    try:
        database.init_db()
        sembrados = database.seed_demo()
        logger.info("Base de datos lista (motor=%s). Registros demo: %s",
                    config.db_type, sembrados)
    except Exception:  # noqa: BLE001
        logger.exception(
            "No se pudo inicializar la base de datos. "
            "Revise las variables de entorno de conexión."
        )


inicializar_datos()


if __name__ == "__main__":
    from werkzeug.serving import run_simple

    logger.info("Motor de base de datos: %s", config.db_type)
    run_simple("0.0.0.0", config.port, app, use_reloader=config.debug, use_debugger=config.debug)