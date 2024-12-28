# Proyecto de Análisis y Carga de Leads en BigQuery

Este proyecto realiza la carga, limpieza y análisis de datos de leads usando Google Cloud Platform (GCP). Se compone de varios scripts en Python que automatizan diferentes etapas del proceso ETL (Extracción, Transformación y Carga), así como un notebook que contiene el análisis y modelado de datos usando técnicas de Machine Learning.

## 🚀 Descripción General

El flujo de trabajo del proyecto se divide en tres partes principales:

1. **Carga de Datos a BigQuery** (`conexion_gcp.py`):
   - Sube un archivo CSV local a BigQuery.
   - Automatiza la conexión a GCP usando credenciales de servicio.

2. **Limpieza y Transformación de Datos** (`sql_limpieza.py`):
   - Realiza consultas SQL para depurar y transformar datos directamente en BigQuery.
   - Elimina columnas innecesarias, maneja valores nulos, elimina duplicados y agrega columnas derivadas.

3. **Análisis y Modelado** (`analisis_datos_leads.ipynb`):
   - Descarga los datos procesados desde BigQuery para realizar análisis exploratorio.
   - Aplica modelos de Machine Learning (XGBoost y Random Forest) para predicción y análisis de leads.

---

## 📂 Estructura del Repositorio
```
|-- conexion_gcp.py                # Carga de datos desde CSV a BigQuery
|-- sql_limpieza.py                # Consultas SQL para limpiar y transformar datos
|-- analisis_datos_leads.ipynb     # Análisis exploratorio y modelado de datos (ML)
|-- requirements.txt               # Librerías necesarias
|-- README.md                      # Documentación del proyecto
```

---

## 📄 Detalle de Archivos

### 1. `conexion_gcp.py`  
- **Función:** Subir archivos CSV a BigQuery.  
- **Características:**
  - Autodetecta el esquema del archivo CSV.
  - Configura la conexión con BigQuery usando credenciales de servicio.
  - Carga datos en la tabla `table_lead_tfg` dentro del dataset `leads`.

### 2. `sql_limpieza.py`  
- **Función:** Realiza limpieza y transformación de datos en BigQuery mediante consultas SQL.  
- **Consultas:**
  1. Elimina columnas innecesarias.
  2. Maneja valores nulos reemplazándolos con valores por defecto.
  3. Elimina duplicados.
  4. Agrega nuevas columnas calculadas.
  5. Filtra datos irrelevantes.

- **Resultado Final:** Crea la tabla `cleaned_leads` que contiene datos listos para el análisis.

### 3. `analisis_datos_leads.ipynb`  
- **Función:** Descarga datos desde BigQuery y realiza análisis exploratorio.  
- **Modelo:** Usa modelos de Machine Learning (XGBoost y Random Forest) para realizar predicciones y análisis de los leads.
- **Automatización:**
  - Descarga automática de credenciales desde GCS.
  - Inicialización automática del cliente de BigQuery.

---

## 🔧 Instalación y Configuración

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

---

## 🛠️ Requisitos

### Archivo `requirements.txt`
```text
google-cloud-storage
google-cloud-bigquery
pandas
numpy
matplotlib
scikit-learn
seaborn
xgboost
``` 

---

## ✨ Ejecución de los Scripts

### 1. Cargar Datos desde CSV a BigQuery
```bash
python conexion_gcp.py
```

### 2. Realizar Limpieza y Transformación de Datos
```bash
python sql_limpieza.py
```

### 3. Análisis y Modelado en el Notebook
Abrir `analisis_datos_leads.ipynb` y ejecutar las celdas en orden.

---

## ⚙️ Automatización de Credenciales en el Notebook
El notebook está configurado para descargar credenciales automáticamente desde Google Cloud Storage (GCS) y autenticar el cliente de BigQuery. No es necesario realizar configuraciones adicionales.

---

## 🚨 Posibles Errores y Soluciones

1. **Error de permisos (403 Forbidden):**  
   - Asegúrate de que la cuenta de servicio tenga permisos de `BigQuery Admin` y `Storage Object Viewer`.
   - Agregar permisos:  
   ```bash
   gcloud projects add-iam-policy-binding future-loader-433707-h4 \
     --member="serviceAccount:tfg-service-account@future-loader-433707-h4.iam.gserviceaccount.com" \
     --role="roles/bigquery.admin"
   ```

2. **Credenciales no encontradas:**  
   - Si el archivo de credenciales no existe, asegúrate de que el bucket `tfg_credencial` tenga acceso público o de que la cuenta tenga permisos adecuados para descargar el archivo.  

   ```bash
   gcloud storage buckets add-iam-policy-binding gs://tfg_credencial \
     --member="allUsers" \
     --role="roles/storage.objectViewer"
   ```

---

## 📈 Resultados Esperados
- **Tablas en BigQuery:**
  - `leads.table_lead_tfg`: Datos brutos cargados desde CSV.
  - `leads.cleaned_leads`: Datos limpios y listos para análisis.
- **Modelos de Machine Learning:**
  - Predicciones de conversión de leads usando Random Forest y XGBoost.
- **Visualizaciones:**
  - Gráficos de distribución, correlación y análisis exploratorio de datos (EDA).

---

## 🚀 Contribuciones y Contacto
Si deseas contribuir o tienes alguna pregunta, no dudes en enviar un Pull Request o contactar al autor del proyecto.

