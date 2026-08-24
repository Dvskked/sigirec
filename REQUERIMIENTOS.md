# Plantilla de requerimientos del proyecto (Clase 06)

> 📋 **Este documento es la INSCRIPCIÓN al hackathon.** Cada equipo lo copia a su repositorio (como
> `REQUERIMIENTOS.md`) y lo entrega lleno en la **Clase 06**.
> **Equipo que no entregue sus requerimientos NO participa por el premio.**

El **PM lidera** esta reunión y es el canal con el instructor (que hace de cliente) para dudas.

---

## 1. Identidad del equipo

- **Nombre del equipo:** SigiDev's
- **Nombre del proyecto:** SIGIREC
- **Integrantes y roles:**
  | Integrante | Rol | Responsable de |
  |-----------|-----|----------------|
  | Camilo Hernandez | ⚙️ DevOps | Repo, Git, CI/CD, despliegue |
  | Miguel Leon | 🎨 Frontend | Interfaz, estilos, interacción |
  | Santiago Sanchez | 🎨 Frontend | Interfaz, estilos, interacción |
  | Karen Forero | 🔧 Backend | Servidor, API, lógica + BD |
  | Andres Forero | 🔧 Backend / 🧭 PM | Servidor, API, lógica + BD / Canal con el cliente, QA, entregas, desbloquear al equipo |

> **Datos** y la **feature clave** las conoce y las trabaja **todo el equipo** (son la estructura del
> proyecto, no un rol aparte).

---

## 2. Visión del proyecto

**La idea en una frase:** _SIGIREC es un sistema de gestión de reciclaje inteligente que usa inteligencia artificial (YOLOv8) para detectar botellas PET, sus tapas y etiquetas mediante la cámara, y recompensa a los usuarios con puntos canjeables (SIGIPUNTOS)._

- **¿Para quién es? (usuarios):** Comunidad educativa SENA (aprendices, instructores y área administrativa) y público externo interesado en reciclar.
- **¿Qué problema resuelve o qué permite hacer?:** Incentiva el reciclaje de botellas PET eliminando el conteo manual: la IA identifica la botella, la tapa y la etiqueta, asigna puntos automáticamente (50 base + 10 tapa + 5 etiqueta), genera comprobantes de cada reciclaje y permite canjear los SIGIPUNTOS por productos ecológicos del catálogo.
- **Visión (a dónde quieren llevarlo):** Convertirnos en la plataforma de reciclaje con recompensas de referencia en instituciones educativas de Colombia, expandiendo los materiales detectables (latas, papel, plásticos varios) e integrando estaciones físicas de acopio con reconocimiento en tiempo real.
- **Modelo:** **B2B2C** — se implementa dentro de instituciones (B2B: el SENA u otras organizaciones) pero el valor lo vive el usuario final (B2C: quien recicla y canjea).
- **¿Cómo generaría valor o dinero?** (si aplica): _Licencias institucionales del software, patrocinios de marcas verdes que financien los premios del catálogo a cambio de visibilidad, y venta de material reciclado recolectado._

---

## 3. Funcionalidades (alcance)

Marca lo que SÍ entra en el MVP (lo mínimo para la Demo Day) y lo que sería "extra si da tiempo".

| Funcionalidad | ¿MVP? | ¿Extra? | Responsable |
|---------------|:-----:|:-------:|-------------|
| Registro e inicio de sesión con roles (Usuario / Administrador) | ✅ | | Backend |
| Escaneo de botella con cámara y detección IA (YOLOv8: botella, tapa, etiqueta) | ✅ | | Backend |
| Sistema de SIGIPUNTOS (50 base + 10 tapa + 5 etiqueta) con historial de movimientos | ✅ | | Backend |
| Comprobante automático por cada reciclaje (SIGI-000001, …) | ✅ | | Backend |
| Catálogo de productos ecológicos y canje de puntos | ✅ | | Frontend + Backend |
| Dashboard de usuario (saldo, historial, estadísticas) | ✅ | | Frontend |
| Panel administrativo (usuarios, puntos, catálogo, auditoría) | ✅ | | Frontend + Backend |
| Auditoría de acciones administrativas (quién hizo qué y cuándo) | ✅ | | Backend |
| Detección en tiempo real continuo desde video (no solo foto capturada) | | ✅ | Backend |
| Notificaciones/logros por rachas de reciclaje | | ✅ | Frontend |
| Ranking de recicladores entre usuarios | | ✅ | Backend |

> Regla: si algo no está en el MVP, **no se construye hasta terminar el MVP**. Primero lo esencial.

---

## 4. Requerimientos técnicos (cómo lo van a hacer)

Deben cubrir **los mínimos del curso**. Marquen qué usarán:

- [x] **Frontend:** HTML semántico + CSS + JavaScript (DOM).
      _Jinja2 como motor de plantillas sobre Flask; JS propio para cámara, dashboard y catálogo (`static/js/`)._
- [ ] **Backend:** Node.js + Express (API con rutas).
      ⚠️ **Nota:** usamos **Python + Flask**, que cumple el mismo rol (servidor + API con rutas): `/login`, `/register`, `/api/escanear`, `/api/registrar-reciclaje`, `/admin/*`, etc.
- [x] **Base de datos:** **MySQL/MariaDB** — tablas listadas abajo.
- [x] **Feature clave:** **Detección de botellas PET con IA (YOLOv8)**: el usuario toma una foto con la cámara y el modelo entrenado identifica botella, tapa y etiqueta, calculando los SIGIPUNTOS ganados automáticamente.
- [ ] **Tiempo real (Socket.IO):** no lo usaremos en el MVP (el escaneo es bajo demanda); como alternativa integraremos **OpenCV + modelo YOLO** que también suma puntos técnicos.
- [x] **Autenticación:** login con contraseña (hash), sesiones con `session` de Flask y control de acceso por rol (USUARIO / ADMINISTRADOR).
- [x] **Otra técnica / API externa:** **YOLOv8n (Ultralytics)** entrenado localmente con dataset propio, **OpenCV** para manejo de cámara/imagen y **PyTorch (CPU)** para inferencia.

**Tablas de datos previstas (ya implementadas):**
```
usuarios(id_usuario, nombre_completo, tipo_documento, numero_identificacion,
         correo, clave_hash, rol, sigipuntos, fecha_registro)
botellas(id_botella, nombre, tipo_material, puntos_base, fecha_registro)
analisis_ia(id_analisis, id_usuario, id_botella, imagen, botella_detectada,
            tapa_detectada, etiqueta_detectada, confianza, puntos_base,
            puntos_tapa, puntos_etiqueta, puntos_totales, estado_analisis,
            modelo_ia, version_modelo, fecha_analisis)
comprobantes_reciclaje(id_comprobante, id_analisis, id_usuario,
                       numero_comprobante, saldo_anterior, puntos_ganados,
                       saldo_nuevo, fecha_comprobante)
movimientos_puntos(id_movimiento, id_usuario, tipo, cantidad, descripcion, fecha)
productos(id_producto, nombre, descripcion, costo_puntos, stock, imagen, estado)
canjes(id_canje, id_producto, id_usuario, total_puntos, fecha_canje)
auditoria(id_auditoria, id_usuario, accion, tabla_afectada, id_registro,
          descripcion, ip, fecha)
```

---

## 5. Requerimientos de despliegue

- **Frontend se desplegará en:** servido desde el mismo backend Flask (plantillas Jinja2 + estáticos) en **Render**.
- **Backend se desplegará en:** **Render** (Web Service con `gunicorn`, configurado vía `render.yaml` + `Procfile`).
- **Base de datos:** MySQL gestionado (ej. Clever Cloud / PlanetScale / Railway) o MariaDB remota; conexión vía variables de entorno.
- **Dominio:** subdominio gratis del host (`sigirec.onrender.com`).
- **CI/CD:** ¿cada `push` actualiza el sitio? **Sí** — Render redespliega automáticamente con cada push a la rama principal.
- **Link del proyecto (cuando exista):** _https://sigirec.onrender.com_ (por definir)

### Costos estimados de servidores
Aunque usemos capas gratuitas para el curso, estimen qué costaría en "producción real":

| Recurso | Proveedor / plan | Costo estimado (mes) |
|---------|------------------|----------------------|
| Hosting del backend (+ modelo IA) | Render Standard (necesita RAM para PyTorch) | USD 25 |
| Base de datos | Railway / Clever Cloud (MySQL pequeño) | USD 5 |
| Dominio propio | Namecheap (.com) | USD 15 (anual) ≈ USD 1.3/mes |
| Almacenamiento de imágenes de análisis | Cloudinary / S3 capa gratuita | USD 0 |
| **Total estimado** | | **~USD 31/mes** |

---

## 6. Plan de trabajo (grueso)

| Clases | Qué esperamos terminar |
|--------|------------------------|
| 07–08 (backend) | Servidor Flask + API base (auth, rutas principales) |
| 09–10 (datos) | Esquema MySQL completo + persistencia de usuarios, puntos y movimientos |
| 11–13 (feature / auth / tiempo real) | Feature clave: escaneo con cámara + detección YOLOv8 + asignación de SIGIPUNTOS y comprobantes |
| 14–15 (integración) | Panel admin + catálogo/canjes + despliegue en Render con CI/CD |
| 16 | Demo lista y ensayada (flujo completo: registro → escaneo → puntos → canje) |

---

## 7. Riesgos y dudas para el cliente (las lleva el PM)

- **Lo que más nos preocupa:**
  - El rendimiento de la inferencia YOLOv8 en la capa gratuita de Render (CPU limitada → respuesta lenta al escanear).
  - La precisión del modelo con condiciones reales (luz, fondos, botellas deformadas): confianzas muy bajas generan falsos positivos/negativos.
  - Límite de almacenamiento/envío del repositorio (pesos `.pt` y dataset son pesados).
- **Preguntas para el instructor (cliente):** _(las hace el PM)_
  - ¿Se acepta backend en Python/Flask aunque el mínimo del curso sea Node.js/Express?
  - ¿La demo puede ejecutarse en local si el despliegue gratuito resulta insuficiente para correr el modelo?
  - ¿Qué política aplicamos ante intentos de fraude (ej. escanear la misma botella varias veces)?
  - ¿Es válido usar una BD MySQL gestionada gratuita externa en lugar de SQLite?

---

> ✅ **Entregable de la Clase 06 (inscripción):** este archivo lleno y subido al repo del equipo
> (commit del PM o del DevOps). Sin él, el equipo no participa por el premio.
