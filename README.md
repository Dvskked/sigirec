# SigiRec

Sistema de gestión de reciclaje inteligente con inteligencia artificial. Detecta botellas PET, tapas y etiquetas mediante YOLOv8 y asigna puntos de reciclaje (SIGIPUNTOS) a los usuarios.

## Funcionalidades

- **Detección IA**: Identifica botellas PET, tapas y etiquetas usando YOLOv8
- **Sistema de puntos**: Asigna SIGIPUNTOS por cada botella reciclada (50 base + 10 tapa + 5 etiqueta)
- **Gestión de usuarios**: Registro, login y perfiles (Aprendiz, Instructor, Área Administrativa, Externo)
- **Panel administrativo**: Gestión de usuarios, puntos, catálogo de productos y auditorías
- **Comprobantes**: Genera comprobante automático por cada reciclaje registrado

## Tecnologías

- Python / Flask
- MySQL
- YOLOv8 (Ultralytics)
- OpenCV
- PyTorch (CPU)

## Requisitos

- Python 3.9+
- MySQL 8.0+
- pip

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

1. Crear la base de datos en MySQL:

```sql
CREATE DATABASE sigirec;
```

2. Importar el esquema SQL (si se dispone del archivo de base de datos).

3. Actualizar la conexión en `conexion.py` si es necesario:

```python
conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="sigirec",
    port=3306
)
```

## Entrenamiento del modelo

```bash
python train.py
```

Entrena YOLOv8n durante 100 épocas con el dataset en `dataset/data.yaml`. Los pesos se guardan en `runs/detect/`.

## Ejecución

```bash
python app.py
```

El servidor se inicia en `http://localhost:5000`.

## Estructura del proyecto

```
SigiRec/
├── app.py              # Aplicación principal Flask
├── conexion.py         # Conexión a MySQL
├── train.py            # Entrenamiento del modelo YOLO
├── camara.py           # Prueba de cámara en tiempo real
├── requirements.txt    # Dependencias
├── database/           # Configuración de base de datos
├── dataset/            # Dataset de entrenamiento
├── runs/               # Pesos del modelo entrenado
├── static/             # Archivos estáticos (CSS, JS, imágenes)
├── templates/          # Plantillas HTML
│   ├── auth/           # Login y registro
│   ├── usuario/        # Vistas de usuario
│   └── admin/          # Panel administrativo
└── uploads/            # Imágenes subidas
```

## Roles de usuario

| Rol | Descripción |
|-----|-------------|
| USUARIO | Acceso estándar al dashboard y escaneo |
| ADMINISTRADOR | Gestión completa del sistema |
