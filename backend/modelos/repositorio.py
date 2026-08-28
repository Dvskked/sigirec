"""Repositorios: lógica de acceso a datos (consultas y escrituras).

Cada función recibe la instancia ``db`` (ver modelos.database) y trabaja
con diccionarios, manteniendo la capa de rutas independiente del motor SQL.
"""

from .database import db, RegistroDuplicado, ViolacionIntegridad  # noqa: F401


# ---------------------------------------------------------------------------
#  Usuarios
# ---------------------------------------------------------------------------
def crear_usuario(nombre, correo, contrasena_hash):
    """Crea un usuario nuevo. Puede lanzar RegistroDuplicado si el correo existe."""
    try:
        id_usuario, _ = db.execute(
            "INSERT INTO usuarios (nombre, correo, contrasena_hash) "
            "VALUES (%s, %s, %s)",
            (nombre.strip(), correo.strip().lower(), contrasena_hash),
        )
    except RegistroDuplicado as exc:
        raise RegistroDuplicado("Ya existe un usuario con ese correo.") from exc
    return obtener_usuario_por_id(id_usuario)


def obtener_usuario_por_id(id_usuario):
    return db.fetch_one(
        "SELECT id_usuario, nombre, correo, fecha_registro "
        "FROM usuarios WHERE id_usuario = %s",
        (id_usuario,),
    )


def obtener_usuario_por_correo(correo):
    return db.fetch_one(
        "SELECT id_usuario, nombre, correo, contrasena_hash, fecha_registro "
        "FROM usuarios WHERE correo = %s",
        (correo.strip().lower(),),
    )


def listar_usuarios():
    return db.fetch_all(
        "SELECT id_usuario, nombre, correo, fecha_registro "
        "FROM usuarios ORDER BY nombre"
    )


# ---------------------------------------------------------------------------
#  Categorías
# ---------------------------------------------------------------------------
def listar_categorias(id_usuario):
    return db.fetch_all(
        "SELECT id_categoria, nombre, tipo FROM categorias "
        "WHERE id_usuario = %s ORDER BY tipo, nombre",
        (id_usuario,),
    )


def crear_categoria(nombre, tipo, id_usuario):
    id_categoria, _ = db.execute(
        "INSERT INTO categorias (nombre, tipo, id_usuario) VALUES (%s, %s, %s)",
        (nombre.strip(), tipo, id_usuario),
    )
    return db.fetch_one(
        "SELECT id_categoria, nombre, tipo FROM categorias WHERE id_categoria = %s",
        (id_categoria,),
    )


def actualizar_categoria(id_categoria, id_usuario, nombre=None, tipo=None):
    campos, params = [], []
    if nombre is not None:
        campos.append("nombre = %s")
        params.append(nombre.strip())
    if tipo is not None:
        campos.append("tipo = %s")
        params.append(tipo)
    if not campos:
        return None
    params += [id_categoria, id_usuario]
    _, afectadas = db.execute(
        f"UPDATE categorias SET {', '.join(campos)} "
        "WHERE id_categoria = %s AND id_usuario = %s",
        tuple(params),
    )
    if afectadas == 0:
        return None
    return db.fetch_one(
        "SELECT id_categoria, nombre, tipo FROM categorias WHERE id_categoria = %s",
        (id_categoria,),
    )


def eliminar_categoria(id_categoria, id_usuario):
    """Elimina una categoría. Puede lanzar ViolacionIntegridad si tiene movimientos."""
    db.execute(
        "DELETE FROM categorias WHERE id_categoria = %s AND id_usuario = %s",
        (id_categoria, id_usuario),
    )


# ---------------------------------------------------------------------------
#  Movimientos (ingresos / gastos)
# ---------------------------------------------------------------------------
def listar_movimientos(id_usuario, desde=None, hasta=None, categoria=None, tipo=None):
    """Consulta movimientos con filtros opcionales y une nombre de categoría."""
    sql = (
        "SELECT m.id_movimiento, m.id_categoria, m.tipo, m.monto, m.fecha, "
        "m.descripcion, c.nombre AS categoria "
        "FROM ingresos_gastos m "
        "JOIN categorias c ON c.id_categoria = m.id_categoria "
        "WHERE m.id_usuario = %s"
    )
    params = [id_usuario]

    if desde:
        sql += " AND m.fecha >= %s"
        params.append(desde)
    if hasta:
        sql += " AND m.fecha <= %s"
        params.append(hasta)
    if categoria:
        sql += " AND m.id_categoria = %s"
        params.append(categoria)
    if tipo in ("ingreso", "gasto"):
        sql += " AND m.tipo = %s"
        params.append(tipo)

    sql += " ORDER BY m.fecha DESC, m.id_movimiento DESC"
    return db.fetch_all(sql, tuple(params))


def crear_movimiento(id_usuario, id_categoria, tipo, monto, fecha, descripcion=None):
    """Crea un movimiento validando que la categoría pertenezca al usuario."""
    categoria = db.fetch_one(
        "SELECT id_categoria FROM categorias "
        "WHERE id_categoria = %s AND id_usuario = %s",
        (id_categoria, id_usuario),
    )
    if not categoria:
        raise ViolacionIntegridad("La categoría no existe o no pertenece al usuario.")

    id_movimiento, _ = db.execute(
        "INSERT INTO ingresos_gastos (id_usuario, id_categoria, tipo, monto, "
        "fecha, descripcion) VALUES (%s, %s, %s, %s, %s, %s)",
        (id_usuario, id_categoria, tipo, monto, fecha, descripcion or None),
    )
    return obtener_movimiento(id_movimiento)


def obtener_movimiento(id_movimiento):
    return db.fetch_one(
        "SELECT m.id_movimiento, m.id_categoria, m.tipo, m.monto, m.fecha, "
        "m.descripcion, c.nombre AS categoria "
        "FROM ingresos_gastos m "
        "JOIN categorias c ON c.id_categoria = m.id_categoria "
        "WHERE m.id_movimiento = %s",
        (id_movimiento,),
    )


def actualizar_movimiento(id_movimiento, id_usuario, campos):
    """Actualiza solo los campos presentes en ``campos``."""
    mapa = {
        "id_categoria": "id_categoria",
        "tipo": "tipo",
        "monto": "monto",
        "fecha": "fecha",
        "descripcion": "descripcion",
    }
    asignaciones, params = [], []
    for clave, columna in mapa.items():
        if clave in campos and campos[clave] is not None:
            asignaciones.append(f"{columna} = %s")
            params.append(campos[clave])
    if not asignaciones:
        return obtener_movimiento(id_movimiento)

    params += [id_movimiento, id_usuario]
    _, afectadas = db.execute(
        f"UPDATE ingresos_gastos SET {', '.join(asignaciones)} "
        "WHERE id_movimiento = %s AND id_usuario = %s",
        tuple(params),
    )
    if afectadas == 0:
        return None
    return obtener_movimiento(id_movimiento)


def eliminar_movimiento(id_movimiento, id_usuario):
    _, afectadas = db.execute(
        "DELETE FROM ingresos_gastos WHERE id_movimiento = %s AND id_usuario = %s",
        (id_movimiento, id_usuario),
    )
    return afectadas > 0