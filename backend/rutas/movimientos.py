"""Rutas de movimientos (ingresos/gastos) con filtros y CRUD (RF03 - RF04)."""

from flask import Blueprint, request

from ..modelos import repositorio as repo
from ..modelos.database import json_ready
from .helpers import (
    ErrorControlador,
    fecha_valida,
    id_entero,
    json_body,
    monto_validado,
    respuesta_error,
    respuesta_ok,
    texto_requerido,
    tipo_valido,
)

movimientos_bp = Blueprint("movimientos", __name__, url_prefix="/api")


@movimientos_bp.get("/movimientos")
def listar_movimientos():
    """Consulta movimientos con filtros: id_usuario, desde, hasta, categoria, tipo."""
    id_usuario = id_entero(request.args.get("id_usuario"), "id_usuario")
    desde = request.args.get("desde") or None
    hasta = request.args.get("hasta") or None
    categoria = id_entero(request.args.get("categoria"), "categoria", requerido=False)
    tipo = request.args.get("tipo") or None

    if desde:
        fecha_valida(desde, "desde")
    if hasta:
        fecha_valida(hasta, "hasta")

    movimientos = repo.listar_movimientos(id_usuario, desde, hasta, categoria, tipo)
    return respuesta_ok(json_ready(movimientos))


@movimientos_bp.post("/movimientos")
def crear_movimiento():
    data = json_body()
    id_usuario = id_entero(data.get("id_usuario"), "id_usuario")
    id_categoria = id_entero(data.get("id_categoria"), "id_categoria")
    tipo = tipo_valido(data.get("tipo"))
    monto = monto_validado(data.get("monto"))
    fecha = fecha_valida(data.get("fecha"))
    descripcion = (data.get("descripcion") or "").strip()[:255] or None

    try:
        movimiento = repo.crear_movimiento(id_usuario, id_categoria, tipo, monto, fecha, descripcion)
    except Exception as exc:
        return respuesta_error(str(exc), 400)

    return respuesta_ok(json_ready([movimiento])[0], 201)


@movimientos_bp.put("/movimientos/<int:id_movimiento>")
def actualizar_movimiento(id_movimiento):
    data = json_body()
    id_usuario = id_entero(data.get("id_usuario"), "id_usuario")
    campos = {}

    if "id_categoria" in data:
        campos["id_categoria"] = id_entero(data.get("id_categoria"), "id_categoria")
    if "tipo" in data:
        campos["tipo"] = tipo_valido(data.get("tipo"))
    if "monto" in data:
        campos["monto"] = monto_validado(data.get("monto"))
    if "fecha" in data:
        campos["fecha"] = fecha_valida(data.get("fecha"))
    if "descripcion" in data:
        campos["descripcion"] = (data.get("descripcion") or "").strip()[:255] or None

    if not campos:
        raise ErrorControlador("No se enviaron campos para actualizar.")

    try:
        movimiento = repo.actualizar_movimiento(id_movimiento, id_usuario, campos)
    except Exception as exc:
        return respuesta_error(str(exc), 400)

    if not movimiento:
        return respuesta_error("Movimiento no encontrado.", 404)
    return respuesta_ok(json_ready([movimiento])[0])


@movimientos_bp.delete("/movimientos/<int:id_movimiento>")
def eliminar_movimiento(id_movimiento):
    id_usuario = id_entero(request.args.get("id_usuario"), "id_usuario")
    eliminado = repo.eliminar_movimiento(id_movimiento, id_usuario)
    if not eliminado:
        return respuesta_error("Movimiento no encontrado.", 404)
    return respuesta_ok({"id_movimiento": id_movimiento})