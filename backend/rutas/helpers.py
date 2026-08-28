"""Helpers compartidos para los controladores de la API."""

from flask import jsonify, request


class ErrorControlador(Exception):
    """Error controlado que se traduce a una respuesta HTTP con JSON."""

    def __init__(self, mensaje, codigo=400):
        super().__init__(mensaje)
        self.mensaje = mensaje
        self.codigo = codigo


def json_body():
    """Devuelve el JSON del request o lanza un ErrorControlador."""
    data = request.get_json(silent=True)
    if data is None or not isinstance(data, dict):
        raise ErrorControlador("Se esperaba un cuerpo JSON válido.")
    return data


def texto_requerido(data, campo, etiqueta=None, max_len=None):
    valor = (data.get(campo) or "").strip()
    if not valor:
        raise ErrorControlador(f"El campo '{campo}' es obligatorio.")
    if max_len and len(valor) > max_len:
        raise ErrorControlador(
            f"El campo '{campo}' no puede superar {max_len} caracteres."
        )
    return valor


def tipo_valido(tipo):
    if tipo not in ("ingreso", "gasto"):
        raise ErrorControlador("El campo 'tipo' debe ser 'ingreso' o 'gasto'.")
    return tipo


def monto_validado(monto, campo="monto"):
    try:
        valor = float(monto)
    except (TypeError, ValueError):
        raise ErrorControlador(f"El campo '{campo}' debe ser un número válido.")
    if valor <= 0:
        raise ErrorControlador(f"El campo '{campo}' debe ser mayor que cero.")
    return round(valor, 2)


def fecha_valida(fecha, campo="fecha"):
    valor = (fecha or "").strip()
    if not valor:
        raise ErrorControlador(f"El campo '{campo}' es obligatorio.")
    partes = valor.split("-")
    if len(partes) != 3 or len(partes[0]) != 4:
        raise ErrorControlador(
            f"El campo '{campo}' debe tener formato AAAA-MM-DD."
        )
    try:
        import datetime

        datetime.date(int(partes[0]), int(partes[1]), int(partes[2]))
    except ValueError:
        raise ErrorControlador(f"El campo '{campo}' es una fecha inválida.")
    return valor


def id_entero(valor, campo="id", requerido=True):
    if valor in (None, ""):
        if requerido:
            raise ErrorControlador(f"El parámetro '{campo}' es obligatorio.")
        return None
    try:
        return int(valor)
    except (TypeError, ValueError):
        raise ErrorControlador(f"El parámetro '{campo}' debe ser un número entero.")


def respuesta_ok(data=None, codigo=200):
    cuerpo = {"ok": True, "data": data}
    return jsonify(cuerpo), codigo


def respuesta_error(mensaje, codigo=400, detalle=None):
    cuerpo = {"ok": False, "error": mensaje}
    if detalle:
        cuerpo["detalle"] = detalle
    return jsonify(cuerpo), codigo