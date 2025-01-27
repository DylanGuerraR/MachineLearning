import pandas as pd
from sdv.single_table import GaussianCopulaSynthesizer
from sdv.metadata import SingleTableMetadata
import numpy as np

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
# Extraer distribución de las 10 ciudades más frecuentes
city_distribution = data['City'].value_counts(normalize=True).head(10)

# Asignar ciudades usando la misma distribución
synthetic_data['City'] = np.random.choice(
    city_distribution.index, 
    size=len(synthetic_data), 
    p=city_distribution.values
)

# 6. --- Personalización de campos con 'Unknown' ---
fields_with_unknowns = ['Specialization', 'What is your current occupation', 'Tags']

for field in fields_with_unknowns:
    field_distribution = data[field].value_counts(normalize=True)
    
    # Asegurarnos de que 'Unknown' esté presente en la lista
    if 'Unknown' not in field_distribution.index:
        field_distribution['Unknown'] = 0.1  # Añadir un 10% si no existe 'Unknown'
    
    # Ajustar los pesos para que sumen 1
    field_distribution /= field_distribution.sum()

    # Asignar valores sintéticos respetando la distribución
    synthetic_data[field] = np.random.choice(
        field_distribution.index,
        size=len(synthetic_data),
        p=field_distribution.values
    )

# 7. --- Filtrado de valores fuera de rango ---
# Filtrar 'Page Views Per Visit' entre 0 y 6
synthetic_data = synthetic_data[
    (synthetic_data['Page Views Per Visit'] >= 0) & 
    (synthetic_data['Page Views Per Visit'] <= 6)
]

# Filtrar 'TotalVisits' entre 0 y 13
synthetic_data = synthetic_data[
    (synthetic_data['TotalVisits'] >= 0) & 
    (synthetic_data['TotalVisits'] <= 13)
]

# 8. Guardar el dataset sintético generado
synthetic_data.to_csv("synthetic_dataset_filtered.csv", index=False)

print("¡Datos sintéticos generados exitosamente con personalización y filtrado!")
