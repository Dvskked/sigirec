-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 19-08-2026 a las 20:21:07
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `sigirec`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `analisis_ia`
--

CREATE TABLE `analisis_ia` (
  `id_analisis` int(10) UNSIGNED NOT NULL,
  `id_usuario` int(10) UNSIGNED DEFAULT NULL,
  `id_botella` int(10) UNSIGNED DEFAULT NULL,
  `imagen` varchar(255) DEFAULT NULL,
  `botella_detectada` tinyint(1) DEFAULT 0,
  `tapa_detectada` tinyint(1) DEFAULT 0,
  `etiqueta_detectada` tinyint(1) DEFAULT 0,
  `confianza` decimal(5,2) DEFAULT NULL,
  `puntos_base` int(10) UNSIGNED DEFAULT 0,
  `puntos_tapa` int(10) UNSIGNED DEFAULT 0,
  `puntos_etiqueta` int(10) UNSIGNED DEFAULT 0,
  `puntos_totales` int(10) UNSIGNED DEFAULT 0,
  `estado_analisis` enum('PENDIENTE','PROCESANDO','IDENTIFICADO','NO_IDENTIFICADO','ERROR') DEFAULT 'PENDIENTE',
  `modelo_ia` varchar(100) DEFAULT NULL,
  `version_modelo` varchar(50) DEFAULT NULL,
  `fecha_analisis` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `analisis_ia`
--

INSERT INTO `analisis_ia` (`id_analisis`, `id_usuario`, `id_botella`, `imagen`, `botella_detectada`, `tapa_detectada`, `etiqueta_detectada`, `confianza`, `puntos_base`, `puntos_tapa`, `puntos_etiqueta`, `puntos_totales`, `estado_analisis`, `modelo_ia`, `version_modelo`, `fecha_analisis`) VALUES
(1, 3, NULL, NULL, 1, 0, 0, 34.02, 50, 0, 0, 50, 'IDENTIFICADO', 'YOLO', 'train-5', '2026-08-15 19:35:15'),
(2, 3, NULL, NULL, 1, 0, 1, 90.30, 50, 0, 5, 55, 'IDENTIFICADO', 'YOLO', 'train-5', '2026-08-15 19:35:33'),
(3, 3, NULL, NULL, 1, 0, 0, 90.74, 50, 0, 0, 50, 'IDENTIFICADO', 'YOLO', 'train-5', '2026-08-15 19:35:50'),
(4, 3, NULL, NULL, 1, 1, 0, 92.49, 50, 10, 0, 60, 'IDENTIFICADO', 'YOLO', 'train-5', '2026-08-15 19:36:10'),
(5, 3, NULL, NULL, 1, 1, 1, 93.79, 50, 10, 5, 65, 'IDENTIFICADO', 'YOLO', 'train-5', '2026-08-15 19:36:39'),
(6, 3, NULL, NULL, 1, 0, 1, 87.80, 50, 0, 5, 55, 'IDENTIFICADO', 'YOLO', 'train-5', '2026-08-15 19:54:08'),
(7, 3, NULL, NULL, 1, 0, 1, 78.65, 50, 0, 5, 55, 'IDENTIFICADO', 'YOLO', 'train-5', '2026-08-15 19:54:18'),
(8, 3, NULL, NULL, 1, 0, 1, 90.09, 50, 0, 5, 55, 'IDENTIFICADO', 'YOLO', 'train-5', '2026-08-16 21:59:31'),
(9, 3, NULL, NULL, 1, 0, 0, 10.31, 50, 0, 0, 50, 'IDENTIFICADO', 'YOLO', 'train-5', '2026-08-17 22:29:40'),
(10, 3, NULL, NULL, 1, 0, 1, 73.73, 50, 0, 5, 55, 'IDENTIFICADO', 'YOLO', 'train-5', '2026-08-17 22:30:49'),
(11, 3, NULL, NULL, 1, 0, 1, 72.96, 50, 0, 5, 55, 'IDENTIFICADO', 'YOLO', 'train-5', '2026-08-17 22:31:21'),
(12, 3, NULL, NULL, 1, 0, 1, 42.93, 50, 0, 5, 55, 'IDENTIFICADO', 'YOLO', 'train-5', '2026-08-18 06:13:45'),
(13, 3, NULL, NULL, 1, 1, 0, 34.69, 50, 10, 0, 60, 'IDENTIFICADO', 'YOLO', 'train-5', '2026-08-18 06:13:59'),
(14, 3, NULL, NULL, 1, 0, 0, 13.11, 50, 0, 0, 50, 'IDENTIFICADO', 'YOLO', 'train-5', '2026-08-18 07:28:51'),
(15, 3, NULL, NULL, 1, 1, 1, 83.99, 50, 10, 5, 65, 'IDENTIFICADO', 'YOLO', 'train-5', '2026-08-18 11:30:19'),
(16, 3, NULL, NULL, 1, 0, 1, 17.14, 50, 0, 5, 55, 'IDENTIFICADO', 'YOLO', 'train-5', '2026-08-18 11:31:04'),
(17, 3, NULL, NULL, 1, 1, 1, 77.39, 50, 10, 5, 65, 'IDENTIFICADO', 'YOLO', 'train-5', '2026-08-18 11:34:28'),
(18, 3, NULL, NULL, 1, 1, 1, 93.78, 50, 10, 5, 65, 'IDENTIFICADO', 'YOLO', 'train-5', '2026-08-18 23:09:34'),
(19, 3, NULL, NULL, 1, 1, 1, 92.16, 50, 10, 5, 65, 'IDENTIFICADO', 'YOLO', 'train-5', '2026-08-18 23:11:01'),
(20, 3, NULL, NULL, 1, 1, 1, 95.08, 50, 10, 5, 65, 'IDENTIFICADO', 'YOLO', 'train-5', '2026-08-18 23:14:16'),
(21, 3, NULL, NULL, 1, 1, 1, 91.68, 50, 10, 5, 65, 'IDENTIFICADO', 'YOLO', 'train-5', '2026-08-18 23:14:25'),
(22, 3, NULL, NULL, 1, 1, 0, 91.44, 50, 10, 0, 60, 'IDENTIFICADO', 'YOLO', 'train-5', '2026-08-18 23:15:36'),
(23, 3, NULL, NULL, 1, 1, 1, 73.60, 50, 10, 5, 65, 'IDENTIFICADO', 'YOLO', 'train-5', '2026-08-19 06:36:42'),
(24, 3, NULL, NULL, 1, 1, 0, 55.56, 50, 10, 0, 60, 'IDENTIFICADO', 'YOLO', 'train-5', '2026-08-19 06:52:45'),
(25, 3, NULL, NULL, 1, 0, 0, 20.10, 50, 0, 0, 50, 'IDENTIFICADO', 'YOLO', 'train-5', '2026-08-19 07:41:27'),
(26, 5, NULL, NULL, 1, 1, 0, 63.59, 50, 10, 0, 60, 'IDENTIFICADO', 'YOLO', 'train-5', '2026-08-19 08:18:04'),
(27, 5, NULL, NULL, 1, 0, 1, 76.11, 50, 0, 5, 55, 'IDENTIFICADO', 'YOLO', 'train-5', '2026-08-19 08:18:59'),
(28, 3, NULL, NULL, 1, 1, 0, 55.32, 50, 10, 0, 60, 'IDENTIFICADO', 'YOLO', 'train-5', '2026-08-19 11:18:25'),
(29, 6, NULL, NULL, 1, 0, 0, 63.85, 50, 0, 0, 50, 'IDENTIFICADO', 'YOLO', 'train-5', '2026-08-19 11:28:18'),
(30, 7, NULL, NULL, 1, 0, 1, 81.08, 50, 0, 5, 55, 'IDENTIFICADO', 'YOLO', 'train-5', '2026-08-19 11:36:37');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auditoria`
--

CREATE TABLE `auditoria` (
  `id_auditoria` int(10) UNSIGNED NOT NULL,
  `id_usuario` int(10) UNSIGNED DEFAULT NULL,
  `accion` varchar(100) NOT NULL,
  `tabla_afectada` varchar(100) DEFAULT NULL,
  `id_registro` int(10) UNSIGNED DEFAULT NULL,
  `descripcion` text DEFAULT NULL,
  `ip` varchar(45) DEFAULT NULL,
  `fecha` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `auditoria`
--

INSERT INTO `auditoria` (`id_auditoria`, `id_usuario`, `accion`, `tabla_afectada`, `id_registro`, `descripcion`, `ip`, `fecha`) VALUES
(1, 1, 'CANJE', 'productos', 1, 'Canje de 500 SIGIPUNTOS por \'Llaverito SIGIREC\' (Usuario ID: 3).', '127.0.0.1', '2026-08-19 11:10:03'),
(2, 1, 'CANJE', 'productos', 5, 'Canje de 1000 SIGIPUNTOS por \'Figura Decorativa SIGIREC\' (Usuario ID: 5).', '127.0.0.1', '2026-08-19 11:17:53'),
(3, 1, 'CANJE', 'productos', 3, 'Canje de 700 SIGIPUNTOS por \'Portalápices Ecológico\' (Usuario ID: 5).', '127.0.0.1', '2026-08-19 11:29:12'),
(4, 1, 'CANJE', 'productos', 3, 'Canje de 700 SIGIPUNTOS por \'Portalápices Ecológico\' (Usuario ID: 5).', '127.0.0.1', '2026-08-19 11:32:22'),
(5, 1, 'CANJE', 'productos', 3, 'Canje de 700 SIGIPUNTOS por \'Portalápices Ecológico\' (Usuario ID: 5).', '127.0.0.1', '2026-08-19 11:37:42');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `botellas`
--

CREATE TABLE `botellas` (
  `id_botella` int(10) UNSIGNED NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `tipo_material` varchar(50) DEFAULT NULL,
  `puntos_base` int(10) UNSIGNED DEFAULT 0,
  `fecha_registro` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `canjes`
--

CREATE TABLE `canjes` (
  `id_canje` int(10) UNSIGNED NOT NULL,
  `id_usuario` int(10) UNSIGNED DEFAULT NULL,
  `total_puntos` int(10) UNSIGNED DEFAULT 0,
  `fecha_canje` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `canjes`
--

INSERT INTO `canjes` (`id_canje`, `id_usuario`, `total_puntos`, `fecha_canje`) VALUES
(1, 3, 500, '2026-08-19 11:10:03'),
(2, 5, 1000, '2026-08-19 11:17:53'),
(3, 5, 700, '2026-08-19 11:29:12'),
(4, 5, 700, '2026-08-19 11:32:22'),
(5, 5, 700, '2026-08-19 11:37:42');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `comprobantes_reciclaje`
--

CREATE TABLE `comprobantes_reciclaje` (
  `id_comprobante` int(10) UNSIGNED NOT NULL,
  `id_analisis` int(10) UNSIGNED DEFAULT NULL,
  `id_usuario` int(10) UNSIGNED DEFAULT NULL,
  `numero_comprobante` varchar(30) NOT NULL,
  `saldo_anterior` int(10) UNSIGNED DEFAULT 0,
  `puntos_ganados` int(10) UNSIGNED DEFAULT 0,
  `saldo_nuevo` int(10) UNSIGNED DEFAULT 0,
  `fecha_comprobante` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `comprobantes_reciclaje`
--

INSERT INTO `comprobantes_reciclaje` (`id_comprobante`, `id_analisis`, `id_usuario`, `numero_comprobante`, `saldo_anterior`, `puntos_ganados`, `saldo_nuevo`, `fecha_comprobante`) VALUES
(1, 1, 3, 'SIGI-000001', 50, 50, 100, '2026-08-15 19:35:15'),
(2, 2, 3, 'SIGI-000002', 100, 55, 155, '2026-08-15 19:35:33'),
(3, 3, 3, 'SIGI-000003', 155, 50, 205, '2026-08-15 19:35:50'),
(4, 4, 3, 'SIGI-000004', 205, 60, 265, '2026-08-15 19:36:10'),
(5, 5, 3, 'SIGI-000005', 265, 65, 330, '2026-08-15 19:36:39'),
(6, 6, 3, 'SIGI-000006', 330, 55, 385, '2026-08-15 19:54:08'),
(7, 7, 3, 'SIGI-000007', 385, 55, 440, '2026-08-15 19:54:18'),
(8, 8, 3, 'SIGI-000008', 440, 55, 495, '2026-08-16 21:59:31'),
(9, 9, 3, 'SIGI-000009', 495, 50, 545, '2026-08-17 22:29:40'),
(10, 10, 3, 'SIGI-000010', 545, 55, 600, '2026-08-17 22:30:49'),
(11, 11, 3, 'SIGI-000011', 600, 55, 655, '2026-08-17 22:31:21'),
(12, 12, 3, 'SIGI-000012', 655, 55, 710, '2026-08-18 06:13:45'),
(13, 13, 3, 'SIGI-000013', 710, 60, 770, '2026-08-18 06:13:59'),
(14, 14, 3, 'SIGI-000014', 0, 50, 50, '2026-08-18 07:28:51'),
(15, 15, 3, 'SIGI-000015', 50, 65, 115, '2026-08-18 11:30:19'),
(16, 16, 3, 'SIGI-000016', 115, 55, 170, '2026-08-18 11:31:04'),
(17, 17, 3, 'SIGI-000017', 170, 65, 235, '2026-08-18 11:34:28'),
(18, 18, 3, 'SIGI-000018', 235, 65, 300, '2026-08-18 23:09:34'),
(19, 19, 3, 'SIGI-000019', 300, 65, 365, '2026-08-18 23:11:01'),
(20, 20, 3, 'SIGI-000020', 365, 65, 430, '2026-08-18 23:14:16'),
(21, 21, 3, 'SIGI-000021', 430, 65, 495, '2026-08-18 23:14:25'),
(22, 22, 3, 'SIGI-000022', 495, 60, 555, '2026-08-18 23:15:36'),
(23, 23, 3, 'SIGI-000023', 555, 65, 620, '2026-08-19 06:36:42'),
(24, 24, 3, 'SIGI-000024', 620, 60, 680, '2026-08-19 06:52:45'),
(25, 25, 3, 'SIGI-000025', 680, 50, 730, '2026-08-19 07:41:27'),
(26, 26, 5, 'SIGI-000026', 0, 60, 60, '2026-08-19 08:18:04'),
(27, 27, 5, 'SIGI-000027', 60, 55, 115, '2026-08-19 08:18:59'),
(28, 28, 3, 'SIGI-000028', 230, 60, 290, '2026-08-19 11:18:25'),
(29, 29, 6, 'SIGI-000029', 0, 50, 50, '2026-08-19 11:28:18'),
(30, 30, 7, 'SIGI-000030', 0, 55, 55, '2026-08-19 11:36:37');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `movimientos_puntos`
--

CREATE TABLE `movimientos_puntos` (
  `id_movimiento` int(10) UNSIGNED NOT NULL,
  `id_usuario` int(10) UNSIGNED DEFAULT NULL,
  `id_analisis` int(10) UNSIGNED DEFAULT NULL,
  `id_canje` int(10) UNSIGNED DEFAULT NULL,
  `tipo_movimiento` enum('RECICLAJE','CANJE','AJUSTE','BONIFICACION','PENALIZACION','REVERSION') NOT NULL,
  `puntos` int(11) NOT NULL,
  `motivo` varchar(255) DEFAULT NULL,
  `id_usuario_admin` int(10) UNSIGNED DEFAULT NULL,
  `fecha_movimiento` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `movimientos_puntos`
--

INSERT INTO `movimientos_puntos` (`id_movimiento`, `id_usuario`, `id_analisis`, `id_canje`, `tipo_movimiento`, `puntos`, `motivo`, `id_usuario_admin`, `fecha_movimiento`) VALUES
(1, 3, NULL, NULL, 'BONIFICACION', 50, 'Prueba', 1, '2026-08-15 10:59:00'),
(2, 3, 1, NULL, 'RECICLAJE', 50, 'Reciclaje detectado por IA: botella', NULL, '2026-08-15 19:35:15'),
(3, 3, 2, NULL, 'RECICLAJE', 55, 'Reciclaje detectado por IA: botella + etiqueta', NULL, '2026-08-15 19:35:33'),
(4, 3, 3, NULL, 'RECICLAJE', 50, 'Reciclaje detectado por IA: botella', NULL, '2026-08-15 19:35:50'),
(5, 3, 4, NULL, 'RECICLAJE', 60, 'Reciclaje detectado por IA: botella + tapa', NULL, '2026-08-15 19:36:10'),
(6, 3, 5, NULL, 'RECICLAJE', 65, 'Reciclaje detectado por IA: botella + tapa + etiqueta', NULL, '2026-08-15 19:36:39'),
(7, 3, 6, NULL, 'RECICLAJE', 55, 'Reciclaje detectado por IA: botella + etiqueta', NULL, '2026-08-15 19:54:08'),
(8, 3, 7, NULL, 'RECICLAJE', 55, 'Reciclaje detectado por IA: botella + etiqueta', NULL, '2026-08-15 19:54:18'),
(9, 3, 8, NULL, 'RECICLAJE', 55, 'Reciclaje detectado por IA: botella + etiqueta', NULL, '2026-08-16 21:59:31'),
(10, 3, 9, NULL, 'RECICLAJE', 50, 'Reciclaje detectado por IA: botella', NULL, '2026-08-17 22:29:40'),
(11, 3, 10, NULL, 'RECICLAJE', 55, 'Reciclaje detectado por IA: botella + etiqueta', NULL, '2026-08-17 22:30:49'),
(12, 3, 11, NULL, 'RECICLAJE', 55, 'Reciclaje detectado por IA: botella + etiqueta', NULL, '2026-08-17 22:31:21'),
(13, 3, 12, NULL, 'RECICLAJE', 55, 'Reciclaje detectado por IA: botella + etiqueta', NULL, '2026-08-18 06:13:45'),
(14, 3, 13, NULL, 'RECICLAJE', 60, 'Reciclaje detectado por IA: botella + tapa', NULL, '2026-08-18 06:13:59'),
(15, 3, NULL, NULL, 'PENALIZACION', -770, 'intercambio de puntos', 1, '2026-08-18 07:14:56'),
(16, 3, 14, NULL, 'RECICLAJE', 50, 'Reciclaje detectado por IA: botella', NULL, '2026-08-18 07:28:51'),
(17, 3, 15, NULL, 'RECICLAJE', 65, 'Reciclaje detectado por IA: botella + tapa + etiqueta', NULL, '2026-08-18 11:30:19'),
(18, 3, 16, NULL, 'RECICLAJE', 55, 'Reciclaje detectado por IA: botella + etiqueta', NULL, '2026-08-18 11:31:04'),
(19, 3, 17, NULL, 'RECICLAJE', 65, 'Reciclaje detectado por IA: botella + tapa + etiqueta', NULL, '2026-08-18 11:34:28'),
(20, 3, 18, NULL, 'RECICLAJE', 65, 'Reciclaje detectado por IA: botella + tapa + etiqueta', NULL, '2026-08-18 23:09:34'),
(21, 3, 19, NULL, 'RECICLAJE', 65, 'Reciclaje detectado por IA: botella + tapa + etiqueta', NULL, '2026-08-18 23:11:01'),
(22, 3, 20, NULL, 'RECICLAJE', 65, 'Reciclaje detectado por IA: botella + tapa + etiqueta', NULL, '2026-08-18 23:14:16'),
(23, 3, 21, NULL, 'RECICLAJE', 65, 'Reciclaje detectado por IA: botella + tapa + etiqueta', NULL, '2026-08-18 23:14:25'),
(24, 3, 22, NULL, 'RECICLAJE', 60, 'Reciclaje detectado por IA: botella + tapa', NULL, '2026-08-18 23:15:36'),
(25, 3, 23, NULL, 'RECICLAJE', 65, 'Reciclaje detectado por IA: botella + tapa + etiqueta', NULL, '2026-08-19 06:36:42'),
(26, 3, 24, NULL, 'RECICLAJE', 60, 'Reciclaje detectado por IA: botella + tapa', NULL, '2026-08-19 06:52:45'),
(27, 3, 25, NULL, 'RECICLAJE', 50, 'Reciclaje detectado por IA: botella', NULL, '2026-08-19 07:41:27'),
(28, 5, 26, NULL, 'RECICLAJE', 60, 'Reciclaje detectado por IA: botella + tapa', NULL, '2026-08-19 08:18:04'),
(29, 5, 27, NULL, 'RECICLAJE', 55, 'Reciclaje detectado por IA: botella + etiqueta', NULL, '2026-08-19 08:18:59'),
(30, 3, NULL, 1, 'CANJE', -500, 'Canje de 500 SIGIPUNTOS por producto: Llaverito SIGIREC', 1, '2026-08-19 11:10:03'),
(31, 5, NULL, NULL, 'BONIFICACION', 5000, 'Prueba', 1, '2026-08-19 11:17:29'),
(32, 5, NULL, 2, 'CANJE', -1000, 'Canje de 1000 SIGIPUNTOS por producto: Figura Decorativa SIGIREC', 1, '2026-08-19 11:17:53'),
(33, 3, 28, NULL, 'RECICLAJE', 60, 'Reciclaje detectado por IA: botella + tapa', NULL, '2026-08-19 11:18:25'),
(34, 6, 29, NULL, 'RECICLAJE', 50, 'Reciclaje detectado por IA: botella', NULL, '2026-08-19 11:28:18'),
(35, 5, NULL, 3, 'CANJE', -700, 'Canje de 700 SIGIPUNTOS por producto: Portalápices Ecológico', 1, '2026-08-19 11:29:12'),
(36, 5, NULL, 4, 'CANJE', -700, 'Canje de 700 SIGIPUNTOS por producto: Portalápices Ecológico', 1, '2026-08-19 11:32:22'),
(37, 7, 30, NULL, 'RECICLAJE', 55, 'Reciclaje detectado por IA: botella + etiqueta', NULL, '2026-08-19 11:36:37'),
(38, 5, NULL, 5, 'CANJE', -700, 'Canje de 700 SIGIPUNTOS por producto: Portalápices Ecológico', 1, '2026-08-19 11:37:42');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `productos`
--

CREATE TABLE `productos` (
  `id_producto` int(10) UNSIGNED NOT NULL,
  `nombre` varchar(150) NOT NULL,
  `descripcion` text DEFAULT NULL,
  `imagen` varchar(255) DEFAULT NULL,
  `costo_puntos` int(10) UNSIGNED NOT NULL,
  `stock` int(10) UNSIGNED DEFAULT 0,
  `fecha_registro` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `productos`
--

INSERT INTO `productos` (`id_producto`, `nombre`, `descripcion`, `imagen`, `costo_puntos`, `stock`, `fecha_registro`) VALUES
(1, 'Llaverito SIGIREC', 'Llaverito impreso en 3D con diseño alusivo a SIGIREC y al reciclaje.', 'llavero-sigirec.png', 500, 9, '2026-08-14 21:10:40'),
(2, 'Mini Maceta Ecológica', 'Mini maceta decorativa impresa en 3D para plantas pequeñas.', 'mini-maceta.png', 620, 8, '2026-08-14 21:10:40'),
(3, 'Portalápices Ecológico', 'Portalápices impreso en 3D con diseño ecológico para escritorio.', 'portalapices.png', 700, 3, '2026-08-14 21:10:40'),
(4, 'Organizador de Escritorio', 'Organizador de escritorio impreso en 3D para guardar útiles pequeños.', 'organizador.png', 850, 5, '2026-08-14 21:10:40'),
(5, 'Figura Decorativa SIGIREC', 'Figura decorativa impresa en 3D con diseño representativo de SIGIREC.', 'figura-sigirec.png', 1000, 2, '2026-08-14 21:10:40');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `id_usuario` int(10) UNSIGNED NOT NULL,
  `numero_identificacion` varchar(30) NOT NULL,
  `nombre_completo` varchar(150) NOT NULL,
  `correo` varchar(150) NOT NULL,
  `telefono` varchar(20) DEFAULT NULL,
  `tipo_usuario` enum('USUARIO','ADMINISTRADOR') NOT NULL DEFAULT 'USUARIO',
  `rol` enum('APRENDIZ','INSTRUCTOR','AREA_ADMINISTRATIVA','EXTERNO') DEFAULT 'APRENDIZ',
  `programa_formacion` varchar(150) DEFAULT NULL,
  `numero_ficha` varchar(30) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`id_usuario`, `numero_identificacion`, `nombre_completo`, `correo`, `telefono`, `tipo_usuario`, `rol`, `programa_formacion`, `numero_ficha`) VALUES
(1, '1099741266', 'Andres', 'siriusplanet76@gmail.com', '3153806797', 'ADMINISTRADOR', 'APRENDIZ', 'Adso', '3139687'),
(3, '1', 'petroskyyyyyyyy', 'asdj@gmail.com', '12313', 'USUARIO', 'EXTERNO', 'sadad', '3242424'),
(5, '1358965789', 'dev', 'habieruduxing@gmail.com', '3158749685', 'USUARIO', 'INSTRUCTOR', 'adso', '31389578'),
(6, '1098638786', 'carlos chaparro', 'correofalso@gmail.com', '3203257689', 'USUARIO', 'INSTRUCTOR', 'Adso', '3136876'),
(7, '12478568', 'karen', 'karen@gmail.com', '3186547525', 'USUARIO', 'APRENDIZ', 'ADSO', '3139687');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `analisis_ia`
--
ALTER TABLE `analisis_ia`
  ADD PRIMARY KEY (`id_analisis`),
  ADD KEY `fk_analisis_usuarios` (`id_usuario`),
  ADD KEY `fk_analisis_botellas` (`id_botella`);

--
-- Indices de la tabla `auditoria`
--
ALTER TABLE `auditoria`
  ADD PRIMARY KEY (`id_auditoria`),
  ADD KEY `fk_auditoria_usuarios` (`id_usuario`);

--
-- Indices de la tabla `botellas`
--
ALTER TABLE `botellas`
  ADD PRIMARY KEY (`id_botella`);

--
-- Indices de la tabla `canjes`
--
ALTER TABLE `canjes`
  ADD PRIMARY KEY (`id_canje`),
  ADD KEY `fk_canjes_usuarios` (`id_usuario`);

--
-- Indices de la tabla `comprobantes_reciclaje`
--
ALTER TABLE `comprobantes_reciclaje`
  ADD PRIMARY KEY (`id_comprobante`),
  ADD KEY `fk_comprobantes_analisis` (`id_analisis`),
  ADD KEY `fk_comprobantes_usuarios` (`id_usuario`);

--
-- Indices de la tabla `movimientos_puntos`
--
ALTER TABLE `movimientos_puntos`
  ADD PRIMARY KEY (`id_movimiento`),
  ADD KEY `fk_movimientos_usuarios` (`id_usuario`),
  ADD KEY `fk_movimientos_analisis` (`id_analisis`),
  ADD KEY `fk_movimientos_canjes` (`id_canje`),
  ADD KEY `fk_movimientos_admin` (`id_usuario_admin`);

--
-- Indices de la tabla `productos`
--
ALTER TABLE `productos`
  ADD PRIMARY KEY (`id_producto`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id_usuario`),
  ADD UNIQUE KEY `id_usuario` (`id_usuario`),
  ADD UNIQUE KEY `numero_identificacion` (`numero_identificacion`),
  ADD UNIQUE KEY `correo` (`correo`),
  ADD UNIQUE KEY `telefono` (`telefono`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `analisis_ia`
--
ALTER TABLE `analisis_ia`
  MODIFY `id_analisis` int(10) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=31;

--
-- AUTO_INCREMENT de la tabla `auditoria`
--
ALTER TABLE `auditoria`
  MODIFY `id_auditoria` int(10) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `botellas`
--
ALTER TABLE `botellas`
  MODIFY `id_botella` int(10) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `canjes`
--
ALTER TABLE `canjes`
  MODIFY `id_canje` int(10) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `comprobantes_reciclaje`
--
ALTER TABLE `comprobantes_reciclaje`
  MODIFY `id_comprobante` int(10) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=31;

--
-- AUTO_INCREMENT de la tabla `movimientos_puntos`
--
ALTER TABLE `movimientos_puntos`
  MODIFY `id_movimiento` int(10) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=39;

--
-- AUTO_INCREMENT de la tabla `productos`
--
ALTER TABLE `productos`
  MODIFY `id_producto` int(10) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id_usuario` int(10) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `analisis_ia`
--
ALTER TABLE `analisis_ia`
  ADD CONSTRAINT `fk_analisis_botellas` FOREIGN KEY (`id_botella`) REFERENCES `botellas` (`id_botella`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_analisis_usuarios` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`) ON DELETE SET NULL ON UPDATE CASCADE;

--
-- Filtros para la tabla `auditoria`
--
ALTER TABLE `auditoria`
  ADD CONSTRAINT `fk_auditoria_usuarios` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`) ON DELETE SET NULL ON UPDATE CASCADE;

--
-- Filtros para la tabla `canjes`
--
ALTER TABLE `canjes`
  ADD CONSTRAINT `fk_canjes_usuarios` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`) ON DELETE SET NULL ON UPDATE CASCADE;

--
-- Filtros para la tabla `comprobantes_reciclaje`
--
ALTER TABLE `comprobantes_reciclaje`
  ADD CONSTRAINT `fk_comprobantes_analisis` FOREIGN KEY (`id_analisis`) REFERENCES `analisis_ia` (`id_analisis`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_comprobantes_usuarios` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`) ON DELETE SET NULL ON UPDATE CASCADE;

--
-- Filtros para la tabla `movimientos_puntos`
--
ALTER TABLE `movimientos_puntos`
  ADD CONSTRAINT `fk_movimientos_admin` FOREIGN KEY (`id_usuario_admin`) REFERENCES `usuarios` (`id_usuario`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_movimientos_analisis` FOREIGN KEY (`id_analisis`) REFERENCES `analisis_ia` (`id_analisis`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_movimientos_canjes` FOREIGN KEY (`id_canje`) REFERENCES `canjes` (`id_canje`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_movimientos_usuarios` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`) ON DELETE SET NULL ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
