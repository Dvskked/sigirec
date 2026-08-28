"""Rutas del módulo analítico: predicción y anomalías (RF08 - RF09)."""

from flask import Blueprint, request

from ..analitica.anomalias import detectar_anomalias
from ..analitica.predictor import predecir_gasto_proximo_mes
from ..modelos import repositorio as repo
from .helpers import id_entero, respuesta_ok

analitica_bp = Blueprint("analitica", __name__, url_prefix="/api")


def _cargar_movimientos(id_usuario):
    return repo.listar_movimientos(id_usuario)


@analitica_bp.get("/analitica/prediccion")
def prediccion():
    """Predicción del gasto del próximo mes por regresión lineal."""
    id_usuario = id_entero(request.args.get("id_usuario"), "id_usuario")
    movimientos = _cargar_movimientos(id_usuario)
    resultado = predecir_gasto_proximo_mes(movimientos)
    resultado["id_usuario"] = id_usuario
    return respuesta_ok(resultado)


@analitica_bp.get("/analitica/anomalias")
def anomalias():
    """Movimientos que se desvían del patrón histórico (Z-Score)."""
    id_usuario = id_entero(request.args.get("id_usuario"), "id_usuario")
    movimientos = _cargar_movimientos(id_usuario)
    return respuesta_ok(detectar_anomalias(movimientos))