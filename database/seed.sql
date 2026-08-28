-- =====================================================================
--  Finanzas Personales - Datos de demostración (MySQL 8.0+)
--
--  Usuario demo:
--    Correo:    ana@example.com
--    Contraseña: 123456
--
--  NOTA: si ejecutas el backend sin ejecutar este archivo, la aplicación
--  genera automáticamente estos mismos datos al primer arranque (SEED_DEMO).
-- =====================================================================

USE finanzas_personales;

-- Posterga las comprobaciones para poder borrar/recrear sin errores
SET FOREIGN_KEY_CHECKS = 0;

DELETE FROM ingresos_gastos;
DELETE FROM categorias;
DELETE FROM usuarios;

-- Reiniciar los contadores AUTO_INCREMENT (opcional, para empezar desde ID 1)
ALTER TABLE ingresos_gastos AUTO_INCREMENT = 1;
ALTER TABLE categorias AUTO_INCREMENT = 1;
ALTER TABLE usuarios AUTO_INCREMENT = 1;

SET FOREIGN_KEY_CHECKS = 1;

-- Usuario de prueba
INSERT INTO usuarios (id_usuario, nombre, correo, contrasena_hash) VALUES
(1, 'Ana Torres', 'ana@example.com', '$2b$12$LL2DAU9Nltm5XObkUeaQVeIwfvmFe58tmfdUROU8N6fL6BmAl63Te');

-- Categorías
INSERT INTO categorias (id_categoria, nombre, tipo, id_usuario) VALUES
(1, 'Salario',          'ingreso', 1),
(2, 'Freelance',        'ingreso', 1),
(3, 'Alimentación',     'gasto',   1),
(4, 'Transporte',       'gasto',   1),
(5, 'Entretenimiento',  'gasto',   1),
(6, 'Salud',            'gasto',   1),
(7, 'Vivienda',         'gasto',   1),
(8, 'Servicios',        'gasto',   1),
(9, 'Educación',        'gasto',   1);

-- Movimientos (8 meses con crecimiento de datos para regresión/anomalías)
INSERT INTO ingresos_gastos (id_usuario, id_categoria, tipo, monto, fecha, descripcion) VALUES
(1, 1, 'ingreso', 2500000, '2026-01-02', 'Pago mensual'),
(1, 7, 'gasto',   700000,  '2026-01-03', 'Arriendo'),
(1, 8, 'gasto',   150000,  '2026-01-05', 'Luz, agua e internet'),
(1, 3, 'gasto',   320000,  '2026-01-06', 'Mercado del mes'),
(1, 4, 'gasto',   90000,   '2026-01-08', 'Transporte semanal'),
(1, 5, 'gasto',   120000,  '2026-01-12', 'Cine y salidas'),
(1, 6, 'gasto',   40000,   '2026-01-15', 'Cita de control'),
(1, 2, 'ingreso', 300000,  '2026-01-18', 'Proyecto web'),
(1, 9, 'gasto',   65000,   '2026-01-22', 'Curso online'),

(1, 1, 'ingreso', 2500000, '2026-02-02', 'Pago mensual'),
(1, 7, 'gasto',   700000,  '2026-02-03', 'Arriendo'),
(1, 8, 'gasto',   155000,  '2026-02-05', 'Luz, agua e internet'),
(1, 3, 'gasto',   290000,  '2026-02-06', 'Mercado del mes'),
(1, 4, 'gasto',   85000,   '2026-02-08', 'Transporte semanal'),
(1, 5, 'gasto',   100000,  '2026-02-13', 'Concierto'),
(1, 6, 'gasto',   45000,   '2026-02-16', 'Farmacia'),
(1, 2, 'ingreso', 450000,  '2026-02-19', 'Diseño de marca'),
(1, 9, 'gasto',   65000,   '2026-02-23', 'Curso online'),

(1, 1, 'ingreso', 2500000, '2026-03-02', 'Pago mensual'),
(1, 7, 'gasto',   700000,  '2026-03-03', 'Arriendo'),
(1, 8, 'gasto',   148000,  '2026-03-05', 'Luz, agua e internet'),
(1, 3, 'gasto',   310000,  '2026-03-06', 'Mercado del mes'),
(1, 4, 'gasto',   95000,   '2026-03-09', 'Transporte y taxi'),
(1, 5, 'gasto',   140000,  '2026-03-14', 'Salida familiar'),
(1, 6, 'gasto',   38000,   '2026-03-16', 'Control médico'),
(1, 2, 'ingreso', 220000,  '2026-03-20', 'Soporte técnico'),
(1, 9, 'gasto',   65000,   '2026-03-24', 'Curso online'),

(1, 1, 'ingreso', 2500000, '2026-04-02', 'Pago mensual'),
(1, 7, 'gasto',   700000,  '2026-04-03', 'Arriendo'),
(1, 8, 'gasto',   160000,  '2026-04-05', 'Luz, agua e internet'),
(1, 3, 'gasto',   335000,  '2026-04-07', 'Mercado del mes'),
(1, 4, 'gasto',   88000,   '2026-04-09', 'Transporte semanal'),
(1, 5, 'gasto',   110000,  '2026-04-13', 'Streaming y salidas'),
(1, 6, 'gasto',   50000,   '2026-04-15', 'Vacunación'),
(1, 2, 'ingreso', 520000,  '2026-04-21', 'App móvil'),
(1, 9, 'gasto',   65000,   '2026-04-24', 'Curso online'),

(1, 1, 'ingreso', 2500000, '2026-05-02', 'Pago mensual'),
(1, 7, 'gasto',   700000,  '2026-05-04', 'Arriendo'),
(1, 8, 'gasto',   145000,  '2026-05-05', 'Luz, agua e internet'),
(1, 3, 'gasto',   305000,  '2026-05-06', 'Mercado del mes'),
(1, 4, 'gasto',   92000,   '2026-05-08', 'Transporte semanal'),
(1, 5, 'gasto',   160000,  '2026-05-14', 'Salida de fin de semana'),
(1, 6, 'gasto',   42000,   '2026-05-16', 'Farmacia'),
(1, 2, 'ingreso', 350000,  '2026-05-20', 'Consultoría'),
(1, 9, 'gasto',   65000,   '2026-05-25', 'Curso online'),

(1, 1, 'ingreso', 2500000, '2026-06-01', 'Pago mensual'),
(1, 7, 'gasto',   700000,  '2026-06-03', 'Arriendo'),
(1, 8, 'gasto',   152000,  '2026-06-05', 'Luz, agua e internet'),
(1, 3, 'gasto',   320000,  '2026-06-05', 'Mercado del mes'),
(1, 4, 'gasto',   90000,   '2026-06-07', 'Transporte semanal'),
(1, 5, 'gasto',   150000,  '2026-06-10', 'Cine y salidas'),
(1, 6, 'gasto',   44000,   '2026-06-16', 'Control médico'),
(1, 2, 'ingreso', 280000,  '2026-06-19', 'Landing page'),
(1, 9, 'gasto',   65000,   '2026-06-24', 'Curso online'),

(1, 1, 'ingreso', 2500000, '2026-07-01', 'Pago mensual'),
(1, 7, 'gasto',   700000,  '2026-07-03', 'Arriendo'),
(1, 8, 'gasto',   158000,  '2026-07-06', 'Luz, agua e internet'),
(1, 3, 'gasto',   300000,  '2026-07-04', 'Mercado del mes'),
(1, 4, 'gasto',   87000,   '2026-07-07', 'Transporte semanal'),
(1, 5, 'gasto',   130000,  '2026-07-12', 'Salida familiar'),
(1, 6, 'gasto',   800000,  '2026-07-15', 'Consulta médica de urgencia'),
(1, 2, 'ingreso', 410000,  '2026-07-20', 'Proyecto de branding'),
(1, 9, 'gasto',   65000,   '2026-07-24', 'Curso online'),

(1, 1, 'ingreso', 2500000, '2026-08-03', 'Pago mensual'),
(1, 7, 'gasto',   700000,  '2026-08-04', 'Arriendo'),
(1, 8, 'gasto',   149000,  '2026-08-06', 'Luz, agua e internet'),
(1, 3, 'gasto',   325000,  '2026-08-06', 'Mercado del mes'),
(1, 4, 'gasto',   93000,   '2026-08-10', 'Transporte semanal'),
(1, 5, 'gasto',   145000,  '2026-08-13', 'Concierto'),
(1, 6, 'gasto',   46000,   '2026-08-15', 'Farmacia'),
(1, 2, 'ingreso', 380000,  '2026-08-21', 'Asesoría técnica'),
(1, 9, 'gasto',   65000,   '2026-08-25', 'Curso online');