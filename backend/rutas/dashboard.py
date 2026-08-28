"""Endpoint combinado del dashboard (una sola petición para toda la vista).

Reutiliza las consultas de resumen y del módulo analítico para que el
frontend cargue KPIs, gráficos, predicción, anomalías y últimos movimientos
en una sola llamada.
"""

from flask import Blueprint, request

from ..analitica import agregaciones
from ..analitica.anomalias import detectar_anomalias
from ..analitica.predictor import predecir_gasto_proximo_mes
from ..modelos import repositorio as repo
from ..modelos.database import json_ready
from .helpers import ErrorControlador, id_entero, respuesta_ok

dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/api")


@dashboard_bp.get("/dashboard")
def dashboard():
    id_usuario = id_entero(request.args.get("id_usuario"), "id_usuario")

    usuario = repo.obtener_usuario_por_id(id_usuario)
    if not usuario:
        raise ErrorControlador("Usuario no encontrado.", 404)

    movimientos = repo.listar_movimientos(id_usuario)

    totales = agregaciones.resumen_totales(movimientos)
    por_categoria = agregaciones.distribucion_por_categoria(movimientos)
    series = agregaciones.series_mensuales(movimientos)
    prediccion = predecir_gasto_proximo_mes(movimientos)
    prediccion["id_usuario"] = id_usuario
    anomalias = detectar_anomalias(movimientos)

    categoria_map = {c["id_categoria"]: c["nombre"] for c in repo.listar_categorias(id_usuario)}

    cuerpo = {
        "usuario": json_ready([usuario])[0],
        "totales": totales,
        "por_categoria": por_categoria,
        "series_mensuales": series,
        "prediccion": prediccion,
        "anomalias": anomalias,
        "categorias": json_ready(repo.listar_categorias(id_usuario)),
        "recientes": json_ready(movimientos[:10]),
        "categorias_nombres": categoria_map,
    }
    return respuesta_ok(cuerpo)