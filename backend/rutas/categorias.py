"""Rutas de gestión de categorías (RF02)."""

from flask import Blueprint, request

from ..modelos import repositorio as repo
from ..modelos.database import ViolacionIntegridad, json_ready
from .helpers import (
    ErrorControlador,
    id_entero,
    json_body,
    respuesta_error,
    respuesta_ok,
    texto_requerido,
    tipo_valido,
)

categorias_bp = Blueprint("categorias", __name__, url_prefix="/api")


@categorias_bp.get("/categorias")
def listar_categorias():
    id_usuario = id_entero(request.args.get("id_usuario"), "id_usuario")
    categorias = repo.listar_categorias(id_usuario)
    return respuesta_ok(json_ready(categorias))


@categorias_bp.post("/categorias")
def crear_categoria():
    data = json_body()
    id_usuario = id_entero(data.get("id_usuario"), "id_usuario")
    nombre = texto_requerido(data, "nombre", max_len=50)
    tipo = tipo_valido(data.get("tipo"))

    # Evita nombres duplicados dentro del mismo usuario.
    existentes = repo.listar_categorias(id_usuario)
    if any(c["nombre"].lower() == nombre.lower() and c["tipo"] == tipo for c in existentes):
        return respuesta_error("Ya existe una categoría con ese nombre y tipo.", 409)

    categoria = repo.crear_categoria(nombre, tipo, id_usuario)
    return respuesta_ok(json_ready([categoria])[0], 201)


@categorias_bp.put("/categorias/<int:id_categoria>")
def actualizar_categoria(id_categoria):
    data = json_body()
    id_usuario = id_entero(data.get("id_usuario"), "id_usuario")
    nombre = data.get("nombre")
    tipo = data.get("tipo")

    if nombre is not None:
        nombre = texto_requerido(data, "nombre", max_len=50)
    if tipo is not None:
        tipo = tipo_valido(tipo)

    categoria = repo.actualizar_categoria(id_categoria, id_usuario, nombre=nombre, tipo=tipo)
    if not categoria:
        return respuesta_error("Categoría no encontrada.", 404)
    return respuesta_ok(json_ready([categoria])[0])


@categorias_bp.delete("/categorias/<int:id_categoria>")
def eliminar_categoria(id_categoria):
    id_usuario = id_entero(request.args.get("id_usuario"), "id_usuario")
    try:
        repo.eliminar_categoria(id_categoria, id_usuario)
    except ViolacionIntegridad as exc:
        return respuesta_error(
            "No se puede eliminar: la categoría tiene movimientos asociados.", 409
        )
    return respuesta_ok({"id_categoria": id_categoria})