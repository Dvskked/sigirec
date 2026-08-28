"""Capa de acceso a datos.

Abstrae MySQL (mysql-connector-python) y SQLite (para desarrollo local)
detrás de una API común. Todas las consultas usan marcadores ``%s`` y los
resultados se devuelven como listas de diccionarios.
"""

import datetime
import decimal
from contextlib import contextmanager

import mysql.connector

from conexion import conectar, conectar_sin_base_datos
from ..config import config


class ErrorBaseDeDatos(Exception):
    """Error genérico de la capa de datos."""


class RegistroDuplicado(Exception):
    """Se intentó insertar un valor único ya existente (p. ej. correo)."""


class ViolacionIntegridad(Exception):
    """Operación rechazada por restricciones de integridad referencial."""


class Database:
    """Envuelve una conexión MySQL o SQLite según la configuración activa."""

    def __init__(self):
        self.db_type = config.db_type

    # ---------------- utilidades internas ----------------
    def _connect(self):
        return conectar()

    def _cursor(self, conn):
        if self.db_type == "mysql":
            return conn.cursor(dictionary=True, buffered=True)
        return conn.cursor()

    @staticmethod
    def _adapt_sql(sql):
        if config.db_type == "sqlite":
            return sql.replace("%s", "?")
        return sql

    @staticmethod
    def _adapt_params(params):
        if config.db_type == "sqlite":
            return tuple(item if item is not None else None for item in (params or ()))
        return tuple(params or ())

    # ---------------- operaciones ----------------
    def fetch_all(self, sql, params=None):
        conn = self._connect()
        try:
            cur = self._cursor(conn)
            cur.execute(self._adapt_sql(sql), self._adapt_params(params))
            rows = cur.fetchall()
            return [dict(r) for r in rows]
        finally:
            conn.close()

    def fetch_one(self, sql, params=None):
        conn = self._connect()
        try:
            cur = self._cursor(conn)
            cur.execute(self._adapt_sql(sql), self._adapt_params(params))
            row = cur.fetchone()
            return dict(row) if row else None
        finally:
            conn.close()

    def execute(self, sql, params=None):
        """Ejecuta una escritura y devuelve (id_insertado, filas_afectadas)."""
        conn = self._connect()
        try:
            cur = self._cursor(conn)
            cur.execute(self._adapt_sql(sql), self._adapt_params(params))
            conn.commit()
            return cur.lastrowid, cur.rowcount
        except Exception as exc:
            try:
                conn.rollback()
            except Exception:
                pass
            self._raise_amigable(exc)
        finally:
            conn.close()

    @staticmethod
    def _raise_amigable(exc):
        if config.db_type == "mysql":
            code = getattr(exc, "errno", None)
            msg = str(exc).lower()
            if code == 1062 or "duplicate" in msg or "1062" in msg:
                raise RegistroDuplicado("Ya existe un registro con ese valor único.") from exc
            if code in (1451, 1452) or "cons. " in msg or "foreign key constraint" in msg:
                raise ViolacionIntegridad(
                    "La operación está restringida por la información relacionada."
                ) from exc
            raise ErrorBaseDeDatos(str(exc)) from exc
        else:  # sqlite
            msg = str(exc).lower()
            if "unique" in msg:
                raise RegistroDuplicado("Ya existe un registro con ese valor único.") from exc
            if "foreign key" in msg:
                raise ViolacionIntegridad(
                    "La operación está restringida por la información relacionada."
                ) from exc
            raise ErrorBaseDeDatos(str(exc)) from exc

    @contextmanager
    def transaccion(self):
        """Contexto para agrupar varias escrituras en una sola transacción."""
        conn = self._connect()
        try:
            cur = _CursorTransaccion(self._cursor(conn))
            yield cur
            conn.commit()
        except Exception as exc:
            try:
                conn.rollback()
            except Exception:
                pass
            self._raise_amigable(exc)
        finally:
            conn.close()


class _CursorTransaccion:
    """Cursor que adapta de forma transparente '%s' a '?' para SQLite."""

    def __init__(self, cursor):
        self._cursor = cursor

    @property
    def lastrowid(self):
        return self._cursor.lastrowid

    @property
    def rowcount(self):
        return self._cursor.rowcount

    def execute(self, sql, params=None):
        return self._cursor.execute(
            Database._adapt_sql(sql), Database._adapt_params(params)
        )


# Instancia global reutilizable.
db = Database()


# ---------------------------------------------------------------------------
#  Normalización de valores para JSON
# ---------------------------------------------------------------------------
def json_ready(filas):
    """Convierte valores no serializables (Decimal, date, datetime) a JSON."""
    if not filas:
        return filas

    def _conv(valor):
        if isinstance(valor, decimal.Decimal):
            return float(valor)
        if isinstance(valor, datetime.datetime):
            return valor.isoformat(sep=" ")[:19]
        if isinstance(valor, datetime.date):
            return valor.isoformat()
        if isinstance(valor, bytes):
            return valor.decode("utf-8", errors="replace")
        return valor

    return [{k: _conv(v) for k, v in fila.items()} for fila in filas]


# ---------------------------------------------------------------------------
#  Creación de esquema y datos de demostración
# ---------------------------------------------------------------------------
_TABLAS_MYSQL = """
CREATE TABLE IF NOT EXISTS usuarios (
    id_usuario      INT AUTO_INCREMENT PRIMARY KEY,
    nombre          VARCHAR(100) NOT NULL,
    correo          VARCHAR(190) NOT NULL UNIQUE,
    contrasena_hash VARCHAR(255) NOT NULL,
    fecha_registro  DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS categorias (
    id_categoria INT AUTO_INCREMENT PRIMARY KEY,
    nombre       VARCHAR(50) NOT NULL,
    tipo         ENUM('ingreso', 'gasto') NOT NULL,
    id_usuario   INT NOT NULL,
    CONSTRAINT fk_cat_usuario FOREIGN KEY (id_usuario)
        REFERENCES usuarios(id_usuario) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS ingresos_gastos (
    id_movimiento   INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario      INT NOT NULL,
    id_categoria    INT NOT NULL,
    tipo            ENUM('ingreso', 'gasto') NOT NULL,
    monto           DECIMAL(12,2) NOT NULL,
    fecha           DATE NOT NULL,
    descripcion     VARCHAR(255),
    fecha_creacion  DATETIME DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_mov_usuario FOREIGN KEY (id_usuario)
        REFERENCES usuarios(id_usuario) ON DELETE CASCADE,
    CONSTRAINT fk_mov_categoria FOREIGN KEY (id_categoria)
        REFERENCES categorias(id_categoria) ON DELETE RESTRICT,
    KEY idx_mov_usuario_fecha (id_usuario, fecha),
    KEY idx_mov_categoria (id_categoria)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
"""

_TABLAS_SQLITE = """
CREATE TABLE IF NOT EXISTS usuarios (
    id_usuario      INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre          TEXT NOT NULL,
    correo          TEXT NOT NULL UNIQUE,
    contrasena_hash TEXT NOT NULL,
    fecha_registro  TEXT DEFAULT (datetime('now', 'localtime'))
);

CREATE TABLE IF NOT EXISTS categorias (
    id_categoria INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre       TEXT NOT NULL,
    tipo         TEXT NOT NULL CHECK (tipo IN ('ingreso', 'gasto')),
    id_usuario   INTEGER NOT NULL,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS ingresos_gastos (
    id_movimiento  INTEGER PRIMARY KEY AUTOINCREMENT,
    id_usuario     INTEGER NOT NULL,
    id_categoria   INTEGER NOT NULL,
    tipo           TEXT NOT NULL CHECK (tipo IN ('ingreso', 'gasto')),
    monto          REAL NOT NULL,
    fecha          TEXT NOT NULL,
    descripcion    TEXT,
    fecha_creacion TEXT DEFAULT (datetime('now', 'localtime')),
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE CASCADE,
    FOREIGN KEY (id_categoria) REFERENCES categorias(id_categoria) ON DELETE RESTRICT
);

CREATE INDEX IF NOT EXISTS idx_mov_usuario_fecha ON ingresos_gastos (id_usuario, fecha);
CREATE INDEX IF NOT EXISTS idx_mov_categoria ON ingresos_gastos (id_categoria);
"""


def init_db():
    """Crea las tablas si no existen. Es idempotente."""
    if config.db_type == "mysql":
        # Si la base de datos no existe aún, intenta crearla.
        try:
            conn = conectar()
            conn.close()
        except mysql.connector.Error:
            temp = conectar_sin_base_datos()
            cur = temp.cursor()
            cur.execute(
                "CREATE DATABASE IF NOT EXISTS `%s` "
                "CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci" % config.mysql_database
            )
            temp.commit()
            cur.close()
            temp.close()

        conn = conectar()
        try:
            cur = conn.cursor()
            for sentencia in _TABLAS_MYSQL.split(";"):
                sentencia = sentencia.strip()
                if sentencia:
                    cur.execute(sentencia)
            conn.commit()
        finally:
            conn.close()
    else:
        conn = conectar()
        try:
            conn.executescript(_TABLAS_SQLITE)
            conn.commit()
        finally:
            conn.close()


# ---------------------------------------------------------------------------
#  Datos de demostración
# ---------------------------------------------------------------------------
_DEMO_USUARIO = ("Ana Torres", "ana@example.com", "123456")

_DEMO_CATEGORIAS = [
    ("Salario", "ingreso"),
    ("Freelance", "ingreso"),
    ("Alimentación", "gasto"),
    ("Transporte", "gasto"),
    ("Entretenimiento", "gasto"),
    ("Salud", "gasto"),
    ("Vivienda", "gasto"),
    ("Servicios", "gasto"),
    ("Educación", "gasto"),
]

_DEMO_MOVIMIENTOS = [
    # (categoria_nombre, tipo, monto, fecha, descripcion)
    ("Salario", "ingreso", 2500000, "2026-01-02", "Pago mensual"),
    ("Vivienda", "gasto", 700000, "2026-01-03", "Arriendo"),
    ("Servicios", "gasto", 150000, "2026-01-05", "Luz, agua e internet"),
    ("Alimentación", "gasto", 320000, "2026-01-06", "Mercado del mes"),
    ("Transporte", "gasto", 90000, "2026-01-08", "Transporte semanal"),
    ("Entretenimiento", "gasto", 120000, "2026-01-12", "Cine y salidas"),
    ("Salud", "gasto", 40000, "2026-01-15", "Cita de control"),
    ("Freelance", "ingreso", 300000, "2026-01-18", "Proyecto web"),
    ("Educación", "gasto", 65000, "2026-01-22", "Curso online"),

    ("Salario", "ingreso", 2500000, "2026-02-02", "Pago mensual"),
    ("Vivienda", "gasto", 700000, "2026-02-03", "Arriendo"),
    ("Servicios", "gasto", 155000, "2026-02-05", "Luz, agua e internet"),
    ("Alimentación", "gasto", 290000, "2026-02-06", "Mercado del mes"),
    ("Transporte", "gasto", 85000, "2026-02-08", "Transporte semanal"),
    ("Entretenimiento", "gasto", 100000, "2026-02-13", "Concierto"),
    ("Salud", "gasto", 45000, "2026-02-16", "Farmacia"),
    ("Freelance", "ingreso", 450000, "2026-02-19", "Diseño de marca"),
    ("Educación", "gasto", 65000, "2026-02-23", "Curso online"),

    ("Salario", "ingreso", 2500000, "2026-03-02", "Pago mensual"),
    ("Vivienda", "gasto", 700000, "2026-03-03", "Arriendo"),
    ("Servicios", "gasto", 148000, "2026-03-05", "Luz, agua e internet"),
    ("Alimentación", "gasto", 310000, "2026-03-06", "Mercado del mes"),
    ("Transporte", "gasto", 95000, "2026-03-09", "Transporte y taxi"),
    ("Entretenimiento", "gasto", 140000, "2026-03-14", "Salida familiar"),
    ("Salud", "gasto", 38000, "2026-03-16", "Control médico"),
    ("Freelance", "ingreso", 220000, "2026-03-20", "Soporte técnico"),
    ("Educación", "gasto", 65000, "2026-03-24", "Curso online"),

    ("Salario", "ingreso", 2500000, "2026-04-02", "Pago mensual"),
    ("Vivienda", "gasto", 700000, "2026-04-03", "Arriendo"),
    ("Servicios", "gasto", 160000, "2026-04-05", "Luz, agua e internet"),
    ("Alimentación", "gasto", 335000, "2026-04-07", "Mercado del mes"),
    ("Transporte", "gasto", 88000, "2026-04-09", "Transporte semanal"),
    ("Entretenimiento", "gasto", 110000, "2026-04-13", "Streaming y salidas"),
    ("Salud", "gasto", 50000, "2026-04-15", "Vacunación"),
    ("Freelance", "ingreso", 520000, "2026-04-21", "App móvil"),
    ("Educación", "gasto", 65000, "2026-04-24", "Curso online"),

    ("Salario", "ingreso", 2500000, "2026-05-02", "Pago mensual"),
    ("Vivienda", "gasto", 700000, "2026-05-04", "Arriendo"),
    ("Servicios", "gasto", 145000, "2026-05-05", "Luz, agua e internet"),
    ("Alimentación", "gasto", 305000, "2026-05-06", "Mercado del mes"),
    ("Transporte", "gasto", 92000, "2026-05-08", "Transporte semanal"),
    ("Entretenimiento", "gasto", 160000, "2026-05-14", "Salida de fin de semana"),
    ("Salud", "gasto", 42000, "2026-05-16", "Farmacia"),
    ("Freelance", "ingreso", 350000, "2026-05-20", "Consultoría"),
    ("Educación", "gasto", 65000, "2026-05-25", "Curso online"),

    ("Salario", "ingreso", 2500000, "2026-06-01", "Pago mensual"),
    ("Vivienda", "gasto", 700000, "2026-06-03", "Arriendo"),
    ("Servicios", "gasto", 152000, "2026-06-05", "Luz, agua e internet"),
    ("Alimentación", "gasto", 320000, "2026-06-05", "Mercado del mes"),
    ("Transporte", "gasto", 90000, "2026-06-07", "Transporte semanal"),
    ("Entretenimiento", "gasto", 150000, "2026-06-10", "Cine y salidas"),
    ("Salud", "gasto", 44000, "2026-06-16", "Control médico"),
    ("Freelance", "ingreso", 280000, "2026-06-19", "Landing page"),
    ("Educación", "gasto", 65000, "2026-06-24", "Curso online"),

    ("Salario", "ingreso", 2500000, "2026-07-01", "Pago mensual"),
    ("Vivienda", "gasto", 700000, "2026-07-03", "Arriendo"),
    ("Servicios", "gasto", 158000, "2026-07-06", "Luz, agua e internet"),
    ("Alimentación", "gasto", 300000, "2026-07-04", "Mercado del mes"),
    ("Transporte", "gasto", 87000, "2026-07-07", "Transporte semanal"),
    ("Entretenimiento", "gasto", 130000, "2026-07-12", "Salida familiar"),
    ("Salud", "gasto", 800000, "2026-07-15", "Consulta médica de urgencia"),
    ("Freelance", "ingreso", 410000, "2026-07-20", "Proyecto de branding"),
    ("Educación", "gasto", 65000, "2026-07-24", "Curso online"),

    ("Salario", "ingreso", 2500000, "2026-08-03", "Pago mensual"),
    ("Vivienda", "gasto", 700000, "2026-08-04", "Arriendo"),
    ("Servicios", "gasto", 149000, "2026-08-06", "Luz, agua e internet"),
    ("Alimentación", "gasto", 325000, "2026-08-06", "Mercado del mes"),
    ("Transporte", "gasto", 93000, "2026-08-10", "Transporte semanal"),
    ("Entretenimiento", "gasto", 145000, "2026-08-13", "Concierto"),
    ("Salud", "gasto", 46000, "2026-08-15", "Farmacia"),
    ("Freelance", "ingreso", 380000, "2026-08-21", "Asesoría técnica"),
    ("Educación", "gasto", 65000, "2026-08-25", "Curso online"),
]


def seed_demo():
    """Inserta datos de demostración únicamente si la base está vacía."""
    if not config.seed_demo:
        return 0

    existente = db.fetch_one("SELECT COUNT(*) AS total FROM usuarios")
    if existente and existente["total"] > 0:
        return 0

    import bcrypt

    contrasena_hash = bcrypt.hashpw(b"123456", bcrypt.gensalt()).decode("utf-8")

    with db.transaccion() as cur:
        cur.execute(
            "INSERT INTO usuarios (nombre, correo, contrasena_hash) VALUES (%s, %s, %s)",
            (_DEMO_USUARIO[0], _DEMO_USUARIO[1], contrasena_hash),
        )
        id_usuario = cur.lastrowid

        id_categoria = {}
        for nombre, tipo in _DEMO_CATEGORIAS:
            cur.execute(
                "INSERT INTO categorias (nombre, tipo, id_usuario) VALUES (%s, %s, %s)",
                (nombre, tipo, id_usuario),
            )
            id_categoria[nombre] = cur.lastrowid

        for nombre, tipo, monto, fecha, descripcion in _DEMO_MOVIMIENTOS:
            cur.execute(
                "INSERT INTO ingresos_gastos (id_usuario, id_categoria, tipo, monto, "
                "fecha, descripcion) VALUES (%s, %s, %s, %s, %s, %s)",
                (id_usuario, id_categoria[nombre], tipo, monto, fecha, descripcion),
            )

    return len(_DEMO_MOVIMIENTOS)