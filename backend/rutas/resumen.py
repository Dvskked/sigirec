"""Rutas de resumen financiero (RF05) que alimentan el dashboard."""

from flask import Blueprint, request

from ..analitica import agregaciones
from ..modelos import repositorio as repo
from ..modelos.database import json_ready
from .helpers import id_entero, respuesta_ok

resumen_bp = Blueprint("resumen", __name__, url_prefix="/api")


@resumen_bp.get("/resumen")
def obtener_resumen():
    """Totales de ingresos, gastos y balance. Acepta id_usuario y mes (AAAA-MM)."""
    id_usuario = id_entero(request.args.get("id_usuario"), "id_usuario")
    mes = (request.args.get("mes") or "").strip()

    movimientos = repo.listar_movimientos(id_usuario)
    if mes:
        movimientos = [m for m in movimientos if str(m["fecha"])[:7] == mes]

    totales = agregaciones.resumen_totales(movimientos)
    return respuesta_ok(totales)


@resumen_bp.get("/resumen/categorias")
def resumen_por_categoria():
    """Distribución del gasto por categoría (para dona Chart.js)."""
    id_usuario = id_entero(request.args.get("id_usuario"), "id_usuario")
    movimientos = repo.listar_movimientos(id_usuario)
    return respuesta_ok(agregaciones.distribucion_por_categoria(movimientos))


@resumen_bp.get("/resumen/mensual")
def resumen_mensual():
    """Series mensuales de ingresos vs. gastos (para línea Chart.js)."""
    id_usuario = id_entero(request.args.get("id_usuario"), "id_usuario")
    movimientos = repo.listar_movimientos(id_usuario)
    return respuesta_ok(agregaciones.series_mensuales(movimientos))