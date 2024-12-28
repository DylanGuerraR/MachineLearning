# En este archivo de python se realizan las consultas de depuración de datos 
# contra el DATA SET que se encuentra en Big Query aprovechando las credenciales 
# y la conexión con la API

from google.cloud import bigquery
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/DYLAN/Desktop/TFG2425/future-loader-433707-h4-60597431aaba.json"

# Inicializar el cliente de BigQuery
client = bigquery.Client()

# 1. Eliminar columnas innecesarias
# Esta consulta selecciona únicamente las columnas relevantes para el análisis y el modelo ML.
# Se crea una nueva tabla 'cleaned_leads' con las columnas esenciales para reducir la carga de procesamiento y evitar datos innecesarios.
query_eliminar_columnas = """
CREATE OR REPLACE TABLE `future-loader-433707-h4.leads.cleaned_leads` AS
SELECT
    `Lead Number`, `Lead Origin`, `Lead Source`, `Converted`,
    `TotalVisits`, `Total Time Spent on Website`, `Page Views Per Visit`,
    `Last Activity`, `Country`, `Specialization`,
    `What is your current occupation`,`A free copy of Mastering The Interview`, `Tags`, `City`,
    `Asymmetrique Activity Index`, `Asymmetrique Profile Index`,
    `Asymmetrique Activity Score`, `Asymmetrique Profile Score`,
    `Last Notable Activity`
FROM
    `future-loader-433707-h4.leads.table_lead_tfg`;
"""

# 2. Manejo de valores nulos
# Se reemplazan los valores nulos de columnas críticas con valores por defecto.
# Esto asegura que el modelo ML no se vea afectado por datos incompletos.
# 'TotalVisits' se reemplaza con 0, 'Country' y 'Specialization' se completan con 'Unknown'.
query_manejar_nulos = """
CREATE OR REPLACE TABLE `future-loader-433707-h4.leads.cleaned_leads` AS
SELECT
    * EXCEPT (`TotalVisits`, `Country`, `Specialization`),
    COALESCE(`TotalVisits`, 0) AS `TotalVisits`,
    COALESCE(`Country`, 'Unknown') AS `Country`,
    COALESCE(`Specialization`, 'Unknown') AS `Specialization`
FROM
    `future-loader-433707-h4.leads.cleaned_leads`;
"""

# 3. Eliminar duplicados
# Se asegura que cada fila sea única eliminando posibles duplicados.
# Esto evita redundancias que podrían sesgar el análisis o el entrenamiento del modelo.
query_eliminar_duplicados = """
CREATE OR REPLACE TABLE `future-loader-433707-h4.leads.cleaned_leads` AS
SELECT DISTINCT * 
FROM `future-loader-433707-h4.leads.cleaned_leads`;
"""

# 4. Crear nueva columna
# Se añade una columna calculada: 'Average Time Per Visit'.
# Esta columna mide el promedio de tiempo por visita para cada lead, proporcionando una métrica adicional para el análisis.
query_nueva_columna = """
CREATE OR REPLACE TABLE `future-loader-433707-h4.leads.cleaned_leads` AS
SELECT
    *,
    (`Total Time Spent on Website` / NULLIF(`TotalVisits`, 0)) AS `Average Time Per Visit`
FROM
    `future-loader-433707-h4.leads.cleaned_leads`;
"""

# 5. Filtrar datos
# Se eliminan filas donde 'Total Time Spent on Website' es 0.
# Esto asegura que se analicen solo leads que hayan interactuado con la web, lo que resulta más relevante para el modelo ML.
query_filtrar_datos = """
CREATE OR REPLACE TABLE `future-loader-433707-h4.leads.cleaned_leads` AS
SELECT *
FROM `future-loader-433707-h4.leads.cleaned_leads`
WHERE `Total Time Spent on Website` > 0;
"""

def ejecutar_consulta(query):
    try:
        # Ejecutar la consulta en BigQuery
        query_job = client.query(query)
        query_job.result()  # Esperar a que la consulta termine
        print("Consulta ejecutada con éxito.")
    except Exception as e:
        print(f"Error al ejecutar la consulta: {e}")

# Lista de consultas con comentarios previos
consultas = [
    query_eliminar_columnas,  # Paso 1: Eliminar columnas irrelevantes
    query_manejar_nulos,      # Paso 2: Manejar valores nulos
    query_eliminar_duplicados, # Paso 3: Eliminar duplicados
    query_nueva_columna,      # Paso 4: Añadir nueva columna
    query_filtrar_datos,      # Paso 5: Filtrar datos no válidos
]

# Ejecutar todas las consultas
for idx, consulta in enumerate(consultas, 1):
    print(f"Ejecutando consulta {idx}...")
    ejecutar_consulta(consulta)

# Consultas de validación
query_validacion_nulls = """
SELECT
    'TotalVisits' AS column_name,
    COUNTIF(`TotalVisits` IS NULL) AS null_count
FROM `future-loader-433707-h4.leads.cleaned_leads`
UNION ALL
SELECT
    'Country',
    COUNTIF(`Country` IS NULL)
FROM `future-loader-433707-h4.leads.cleaned_leads`
UNION ALL
SELECT
    'Specialization',
    COUNTIF(`Specialization` IS NULL)
FROM `future-loader-433707-h4.leads.cleaned_leads`;
"""

query_validacion_estadisticas = """
SELECT
    COUNT(*) AS total_rows,
    COUNT(DISTINCT `Lead Number`) AS unique_leads,
    AVG(`TotalVisits`) AS avg_visits,
    AVG(`Total Time Spent on Website`) AS avg_time,
    AVG(`Page Views Per Visit`) AS avg_page_views
FROM `future-loader-433707-h4.leads.cleaned_leads`;
"""

# Función para ejecutar una consulta y mostrar los resultados
def ejecutar_y_mostrar_resultados(query, limite=20):
    try:
        # Ejecutar la consulta en BigQuery
        query_job = client.query(query)
        results = query_job.result()
        df = results.to_dataframe()  # Convertir los resultados a un DataFrame
        print(df.head(limite))       # Mostrar solo las primeras filas
    except Exception as e:
        print(f"Error al ejecutar la consulta: {e}")

# Ejecutar y mostrar los resultados
print("Validación de valores nulos:")
ejecutar_y_mostrar_resultados(query_validacion_nulls)

print("\nEstadísticas de las columnas:")
ejecutar_y_mostrar_resultados(query_validacion_estadisticas)
