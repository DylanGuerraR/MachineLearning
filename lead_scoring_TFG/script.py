from google.cloud import storage
import os

# Configuración del bucket y credenciales
BUCKET_NAME = "tfg_credencial"
CREDENTIALS_FILE = "tfg-key.json"
LOCAL_CREDENTIALS_PATH = "/tmp/credentials.json"


def download_credentials():
    client = storage.Client()
    bucket = client.bucket(BUCKET_NAME)
    blob = bucket.blob(CREDENTIALS_FILE)

    print("Descargando credenciales desde GCS...")
    blob.download_to_filename(LOCAL_CREDENTIALS_PATH)
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = LOCAL_CREDENTIALS_PATH
    print("Credenciales descargadas y configuradas.")

# Descargar credenciales
download_credentials()

# Inicializar cliente de BigQuery
from google.cloud import bigquery
client = bigquery.Client()

# Ejecutar consulta de prueba
query = "SELECT * FROM `future-loader-433707-h4.leads.cleaned_leads` LIMIT 10"
df = client.query(query).to_dataframe()

print(df.head())