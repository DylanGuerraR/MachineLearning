from google.cloud import bigquery
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/DYLAN/Desktop/TFG2425/future-loader-433707-h4-60597431aaba.json"

# Configurar el cliente
client = bigquery.Client()

# Listar datasets en tu proyecto
datasets = list(client.list_datasets())
if datasets:
    print("Datasets disponibles:")
    for dataset in datasets:
        print(f"- {dataset.dataset_id}")
else:
    print("No hay datasets disponibles en este proyecto.")


# Configurar la ruta del archivo CSV
file_path = "/Users/DYLAN/Desktop/TFG2425/synthetic_dataset_filtered.csv"

# Configurar los parámetros de la carga
job_config = bigquery.LoadJobConfig(
    source_format=bigquery.SourceFormat.CSV,
    skip_leading_rows=1,  # Omitir el encabezado del CSV
    autodetect=True       # Detectar automáticamente el esquema
)

# ID de la tabla destino (formato: "project_id.dataset_id.table_id")
table_id = "future-loader-433707-h4.leads.table_lead_tfg"


# Subir el archivo CSV a BigQuery
with open(file_path, "rb") as source_file:
    job = client.load_table_from_file(
        source_file,  # Archivo de origen
        table_id,     # ID de la tabla destino
        job_config=job_config
    )

# Esperar a que el trabajo de carga termine
job.result()

# Confirmar que los datos fueron cargados correctamente
table = client.get_table(table_id)
print(f"Se cargaron {table.num_rows} filas a la tabla {table_id}.")