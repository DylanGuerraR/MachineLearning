#En este archivo de python se realizan las consultas de depuración de datos contra el DATA SET que se encuentra en Big Query aprovechando las credenciales y la conexión con la API

from google.cloud import bigquery
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/DYLAN/Desktop/TFG2425/future-loader-433707-h4-60597431aaba.json"

# Inicializar el cliente de BigQuery
client = bigquery.Client()

#1
query_eliminar_columnas = """
CREATE OR REPLACE TABLE `future-loader-433707-h4.leads.cleaned_leads` AS
SELECT
    `Lead Number`, `Lead Origin`, `Lead Source`, `Converted`,
    `TotalVisits`, `Total Time Spent on Website`, `Page Views Per Visit`,
    `Last Activity`, `Country`, `Specialization`,
    `What is your current occupation`, `Tags`, `City`,
    `Asymmetrique Activity Index`, `Asymmetrique Profile Index`,
    `Asymmetrique Activity Score`, `Asymmetrique Profile Score`,
    `Last Notable Activity`
FROM
    `future-loader-433707-h4.leads.table_lead_tfg`;
"""
#2
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
#3
query_eliminar_duplicados = """
CREATE OR REPLACE TABLE `future-loader-433707-h4.leads.cleaned_leads` AS
SELECT DISTINCT * 
FROM `future-loader-433707-h4.leads.cleaned_leads`;
"""
#4
query_nueva_columna = """
CREATE OR REPLACE TABLE `future-loader-433707-h4.leads.cleaned_leads` AS
SELECT
    *,
    (`Total Time Spent on Website` / NULLIF(`TotalVisits`, 0)) AS `Average Time Per Visit`
FROM
    `future-loader-433707-h4.leads.cleaned_leads`;
"""
#5
query_filtrar_datos = """
CREATE OR REPLACE TABLE `future-loader-433707-h4.leads.cleaned_leads` AS
SELECT *
FROM `future-loader-433707-h4.leads.cleaned_leads`
WHERE `Total Time Spent on Website` > 0;
"""
#6
query_dividir_datasets = """
CREATE OR REPLACE TABLE `future-loader-433707-h4.leads.training_set` AS
SELECT *
FROM `future-loader-433707-h4.leads.cleaned_leads`
WHERE MOD(ABS(FARM_FINGERPRINT(CAST(`Lead Number` AS STRING))), 10) < 8;

CREATE OR REPLACE TABLE `future-loader-433707-h4.leads.test_set` AS
SELECT *
FROM `future-loader-433707-h4.leads.cleaned_leads`
WHERE MOD(ABS(FARM_FINGERPRINT(CAST(`Lead Number` AS STRING))), 10) >= 8;
"""
def ejecutar_consulta(query):
    try:
        # Ejecutar la consulta en BigQuery
        query_job = client.query(query)
        query_job.result()  # Esperar a que la consulta termine
        print("Consulta ejecutada con éxito.")
    except Exception as e:
        print(f"Error al ejecutar la consulta: {e}")

# Lista de consultas
consultas = [
    query_eliminar_columnas,
    query_manejar_nulos,
    query_eliminar_duplicados,
    query_nueva_columna,
    query_filtrar_datos,
    query_dividir_datasets
]

# Ejecutar todas las consultas
for idx, consulta in enumerate(consultas, 1):
    print(f"Ejecutando consulta {idx}...")
    ejecutar_consulta(consulta)

# Validar las consultas y las dependencias
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