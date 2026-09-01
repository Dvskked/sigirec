# SigiRec

Sistema de gestión de reciclaje inteligente con inteligencia artificial. Detecta botellas PET, tapas y etiquetas mediante YOLOv8 y asigna puntos de reciclaje (SIGIPUNTOS) a los usuarios, quienes pueden canjearlos por productos ecológicos del catálogo.

Desarrollado por el equipo **SigiDev's** para la comunidad educativa SENA (aprendices, instructores y área administrativa) y público externo.

## Funcionalidades

### Usuario
- **Registro e inicio de sesión** con número de identificación y roles (Aprendiz, Instructor, Área Administrativa, Externo)
- **Detección IA**: escanea botellas PET mediante la cámara usando un modelo YOLOv8 entrenado con dataset propio; identifica botella, tapa y etiqueta
- **Sistema de SIGIPUNTOS**: asigna puntos automáticamente según lo detectado (50 base + 10 tapa + 5 etiqueta)
- **Comprobantes de reciclaje**: genera automáticamente un comprobante numerado (SIGI-XXXXXX) por cada reciclaje registrado
- **Catálogo / Tienda**: canjea SIGIPUNTOS por productos ecológicos
- **Dashboard**: saldo de puntos, botellas recicladas, puntos obtenidos y último reciclaje
- **Comprobantes de canje**: numeración CANJ-XXXXXX

### Administrador
- **Panel administrativo** con estadísticas globales (usuarios, escaneos IA, puntos entregados, productos)
- **Gestión de usuarios**: crear, editar y eliminar usuarios; asignar rol y tipo de cuenta
- **Gestión de puntos**: agregar (bonificación) o quitar (penalización) SIGIPUNTOS manualmente
- **Gestión de productos / catálogo**: administrar catálogo de canje
- **Registro de reciclajes**: historial completo de análisis IA y comprobantes
- **Movimientos y canjes**: gestionar el intercambio de puntos por productos desde el panel
- **Auditoría**: registro de todas las acciones administrativas (quién, qué, cuándo e IP), usuarios nuevos, canjes recientes, análisis IA recientes, movimientos de puntos y **ranking** de recicladores
- **Ranking**: top de usuarios con más SIGIPUNTOS

## Tecnologías

### Backend
- Python 3.11 / Flask
- MySQL (gestionado en Clever Cloud)
- gunicorn (servidor de producción)

### IA / Visión
- YOLOv8 (Ultralytics)
- OpenCV
- PyTorch (CPU)

### Frontend
- HTML / CSS / JavaScript (DOM)
- Jinja2 (motor de plantillas)

### Desktop / Distribución
- Electron (aplicación de escritorio)
- PyInstaller (empaquetado del backend Python)
- electron-builder (instalador NSIS para Windows)

### Despliegue
- Render (Web Service, configurado con `render.yaml` y `Procfile`)
- Clever Cloud (base de datos MySQL)

## Estructura del proyecto

```
SigiRec/
├── app.py              # Aplicación principal Flask (rutas, API, lógica)
├── conexion.py         # Conexión a MySQL (Clever Cloud)
├── train.py            # Entrenamiento del modelo YOLO
├── camara.py           # Prueba de cámara en tiempo real
├── main.js             # Aplicación de escritorio Electron
├── app.spec            # Configuración de empaquetado PyInstaller
├── requirements.txt    # Dependencias Python
├── runtime.txt         # Versión de Python para despliegue
├── Procfile            # Comando de inicio en Render
├── render.yaml         # Configuración del despliegue en Render
├── package.json        # Configuración de Electron / electron-builder
├── yolov8n.pt          # Pesos base de YOLOv8n
├── runs/detect/        # Pesos del modelo entrenado (train-5/best.pt)
├── static/             # Archivos estáticos (CSS, JS, imágenes)
├── templates/          # Plantillas Jinja2
│   ├── auth/           # Login y registro
│   ├── usuario/        # Dashboard, escaneo, catálogo, comprobantes
│   └── admin/          # Panel administrativo
├── build/              # Artefactos de electron-builder
└── dist/               # Aplicación empaquetada (Electron + PyInstaller)
```

## Requisitos

- Python 3.9+
- MySQL 8.0+
- pip
- Node.js 18+ y npm (solo para construir la app de escritorio)

## Instalación

```bash
# Clonar el repositorio
git clone <url-del-repositorio>
cd SigiRec

# Crear entorno virtual
python -m venv venv
venv\Scripts\activate   # Windows
# source venv/bin/activate  # Linux/Mac

# Instalar dependencias
pip install -r requirements.txt
```

## Configuración de la base de datos

1. Crear la base de datos en MySQL (local):

```sql
CREATE DATABASE sigirec;
```

2. Importar el esquema SQL (`sigirec (3).sql`) si se dispone de él.

3. Actualizar la conexión en `conexion.py` (por defecto apunta a una instancia gestionada en Clever Cloud):

```python
conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="sigirec",
    port=3306
)
```

## Ejecución en modo web

```bash
python app.py
```

El servidor arranca en `http://localhost:5000`. El modelo de IA se carga desde `runs/detect/train-5/weights/best.pt`; si no está disponible, las funciones de escaneo quedan inhabilitadas con un mensaje de error.

## Ejecución como aplicación de escritorio (Electron)

La app combina un backend Flask (Python) con una ventana Electron (frontend).

**Modo desarrollo:**

```bash
npm install
npm start   # inicia Python (app.py) y abre la ventana de Electron
```

**Generar instalador de Windows (NSIS):**

```bash
# 1. Empaquetar el backend Python con PyInstaller
pyinstaller app.spec

# 2. Crear el instalador de Electron
npm run dist
```

El instalador se genera en la carpeta `dist/`.

## Entrenamiento del modelo

```bash
python train.py
```

Entrena YOLOv8n con el dataset propio. Los pesos se guardan en `runs/detect/`. El modelo usado por la aplicación está en `runs/detect/train-5/weights/best.pt`.

## Despliegue en Render

Definido en `render.yaml` y `Procfile`. La conexión a la base de datos se realiza mediante variables de entorno cuando está disponible, y Render redespliega automáticamente con cada push a la rama principal.

- **URL de producción:** `https://sigirec.onrender.com`
- **CORS:** configura los orígenes permitidos con la variable de entorno `CORS_ORIGINS` (por defecto incluye el dominio de Render).

## Roles de usuario

| Rol | Descripción |
|-----|-------------|
| USUARIO | Acceso al dashboard, escaneo, catálogo y canje |
| ADMINISTRADOR | Gestión completa del sistema (usuarios, puntos, catálogo, canjes, auditoría) |

Los perfiles de registro (Aprendiz, Instructor, Área Administrativa y Externo) permiten identificar el tipo de usuario dentro de la institución.
