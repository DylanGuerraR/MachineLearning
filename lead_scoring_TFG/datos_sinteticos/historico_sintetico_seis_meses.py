import pandas as pd
from sdv.single_table import GaussianCopulaSynthesizer
from sdv.metadata import SingleTableMetadata
import numpy as np
from datetime import timedelta, date

# 1. Cargar el dataset original
csv_path = "/Users/DYLAN/Desktop/TFG2425/Leads.csv"  # Path a tu CSV original
data = pd.read_csv(csv_path)

# 2. Crear la metadata para el dataset
metadata = SingleTableMetadata()
metadata.detect_from_dataframe(data)

# 3. Inicializar y entrenar el modelo Gaussian Copula
synthesizer = GaussianCopulaSynthesizer(metadata)
synthesizer.fit(data)

# 4. Generar datos sintéticos
synthetic_data = synthesizer.sample(300000)  # Generar 300,000 filas

# 5. --- Personalización de 'City' ---
city_distribution = data['City'].value_counts(normalize=True).head(10)
synthetic_data['City'] = np.random.choice(
    city_distribution.index, 
    size=len(synthetic_data), 
    p=city_distribution.values
)

# 6. --- Personalización de campos con 'Unknown' ---
fields_with_unknowns = ['Specialization', 'What is your current occupation', 'Tags']

for field in fields_with_unknowns:
    field_distribution = data[field].value_counts(normalize=True)
    if 'Unknown' not in field_distribution.index:
        field_distribution['Unknown'] = 0.1
    field_distribution /= field_distribution.sum()
    synthetic_data[field] = np.random.choice(
        field_distribution.index,
        size=len(synthetic_data),
        p=field_distribution.values
    )

# 7. --- Filtrado de valores fuera de rango ---
synthetic_data = synthetic_data[
    (synthetic_data['Page Views Per Visit'] >= 0) & 
    (synthetic_data['Page Views Per Visit'] <= 6)
]
synthetic_data = synthetic_data[
    (synthetic_data['TotalVisits'] >= 0) & 
    (synthetic_data['TotalVisits'] <= 13)
]

# 8. --- Añadir fechas realistas con patrones estacionales ---
start_date = date(2024, 1, 24)
end_date = date(2024, 12, 24)
date_range = [start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1)]

peak_months = [8, 9]
december_drop = [12]

# Asignar fechas asegurando una para cada fila
dates = []
for _ in range(len(synthetic_data)):
    while True:
        random_date = np.random.choice(date_range)
        month = random_date.month
        if (month in peak_months and np.random.rand() < 0.6) or \
           (month in december_drop and np.random.rand() < 0.2) or \
           (month not in peak_months + december_drop):
            dates.append(random_date)
            break

synthetic_data = synthetic_data.iloc[:len(dates)].copy()
synthetic_data['Date'] = dates

# 9. Guardar el dataset sintético generado
synthetic_data.to_csv("synthetic_dataset_with_dates.csv", index=False)

print("¡Datos sintéticos generados exitosamente con fechas realistas y patrones estacionales!")
