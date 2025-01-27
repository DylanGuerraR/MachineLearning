import pandas as pd

# Ruta del archivo CSV
csv_path = "C:/Users/DYLAN/Desktop/REPOS/MachineLearning/lead_scoring_TFG/historico_predecido_ML/final_historical_with_xgb_predictions.csv"

# Cargar el archivo CSV
data = pd.read_csv(csv_path)

# Renombrar el campo problemático
data = data.rename(columns={
    'Specialization_Banking, Investment And Insurance': "Specialization_Banking_Investment_And_Insurance"
})

# Guardar el CSV modificado
output_path = "C:/Users/DYLAN/Desktop/REPOS/MachineLearning/lead_scoring_TFG/historico_predecido_ML/final_historical_with_xgb_predictions_cleaned.csv"
data.to_csv(output_path, index=False)

print(f"✅ Archivo modificado guardado en: {output_path}")
