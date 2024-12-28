
# Proyecto de Automatización con BigQuery y Google Cloud Storage

Este proyecto permite automatizar la descarga de credenciales desde Google Cloud Storage (GCS) y ejecutar consultas en BigQuery usando una cuenta de servicio. El objetivo es que cualquier persona que clone el repositorio pueda ejecutarlo sin necesidad de configurar manualmente las credenciales.

## 🚀 Requisitos
- Python 3.8 o superior
- Google Cloud CLI (`gcloud`) instalado y autenticado
- Permisos de acceso a los recursos de Google Cloud (GCS y BigQuery)

## 📂 Instalación y Configuración

### 1. Clonar el Repositorio
```bash
git clone <URL_DEL_REPOSITORIO>
cd <NOMBRE_DEL_REPOSITORIO>
```

### 2. Crear un Entorno Virtual (Opcional pero Recomendado)
```bash
python -m venv gauss-entorno
source gauss-entorno/bin/activate  # Linux/Mac
```

### 3. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 4. Ejecutar el Script Principal
```bash
python script.py
```

---

## 🔧 ¿Qué Hace el Script?
1. **Descarga credenciales desde un bucket de GCS.**
2. **Autentica automáticamente usando una cuenta de servicio.**
3. **Ejecuta una consulta de prueba en BigQuery y muestra los resultados.**

---

## ⚙️ Configuración Automática
El script descarga las credenciales desde un bucket de GCS y configura automáticamente `GOOGLE_APPLICATION_CREDENTIALS`.

Si necesitas modificar el nombre del archivo de credenciales o el bucket:
- **Archivo:** `script.py`
- **Líneas a modificar:**
```python
BUCKET_NAME = "tfg_credencial"
CREDENTIALS_FILE = "future-loader-433707-h4-9a3dca70b7fe.json"
```

---

## 📄 Estructura del Repositorio
```
|-- script.py  # Script principal
|-- requirements.txt  # Dependencias necesarias
|-- README.md  # Documentación del proyecto
```

---

## 🛠️ Problemas Comunes y Soluciones

### 1. Error 403: Permisos Insuficientes
Si recibes un error de permisos al acceder al bucket o a BigQuery:
```bash
gcloud storage buckets add-iam-policy-binding tfg_credencial   --member="serviceAccount:dylanbq@future-loader-433707-h4.iam.gserviceaccount.com"   --role="roles/storage.objectViewer"
```

### 2. El Bucket o Archivo No Existen
Verifica que el archivo de credenciales está en GCS:
```bash
gsutil ls gs://tfg_credencial/
```
Si el archivo no aparece, súbelo:
```bash
gsutil cp /ruta/local/future-loader-433707-h4-9a3dca70b7fe.json gs://tfg_credencial/
```

---

## ✨ ¡Listo para Ejecutar!
Ahora cualquier usuario puede clonar este repositorio y ejecutar consultas en BigQuery sin configuraciones adicionales.
