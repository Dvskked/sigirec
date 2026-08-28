-- =====================================================================
--  Finanzas Personales - Esquema de base de datos (MySQL 8.0+)
--  Modelo normalizado (3FN) con índices para el módulo analítico.
-- =====================================================================
-- NOTA: Si tu proveedor ya crea la base (p. ej. Railway/Aiven), omite este
-- bloque y ejecuta directamente la sección de tablas en esa base.
-- =====================================================================

CREATE DATABASE IF NOT EXISTS finanzas_personales
  CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE finanzas_personales;

-- -------------------------------------------------------------------
-- Tabla de usuarios
-- -------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS usuarios (
    id_usuario      INT AUTO_INCREMENT PRIMARY KEY,
    nombre          VARCHAR(100) NOT NULL,
    correo          VARCHAR(190) NOT NULL UNIQUE,
    contrasena_hash VARCHAR(255) NOT NULL,
    fecha_registro  DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -------------------------------------------------------------------
-- Tabla de categorías (pertenecen a un usuario)
-- -------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS categorias (
    id_categoria    INT AUTO_INCREMENT PRIMARY KEY,
    nombre          VARCHAR(50) NOT NULL,
    tipo            ENUM('ingreso', 'gasto') NOT NULL,
    id_usuario      INT NOT NULL,
    CONSTRAINT fk_cat_usuario FOREIGN KEY (id_usuario)
        REFERENCES usuarios(id_usuario) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -------------------------------------------------------------------
-- Tabla de movimientos (ingresos y gastos)
-- -------------------------------------------------------------------
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

-- NOTA: la aplicación también crea estas tablas automáticamente al arrancar
-- (CREATE TABLE IF NOT EXISTS), por lo que no es obligatorio ejecutar
-- este script manualmente.