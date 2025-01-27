import pandas as pd
from joblib import load

# Cargar el modelo XGBoost
xgb_model = load("C:/Users/DYLAN/Desktop/Modelos DE ML terminados/xgb_model.pkl")

# Cargar los datos históricos preparados
historical_data = pd.read_csv("C:/Users/DYLAN/Desktop/REPOS/MachineLearning/lead_scoring_TFG/datos_sinteticos/historico_preparado.csv")

# Lista de columnas utilizadas durante el entrenamiento del modelo XGBoost
columns_used_for_training = [
    'Lead Number', 'Total Time Spent on Website', 'Page Views Per Visit',
    'A free copy of Mastering The Interview', 'TotalVisits',
    'Average Time Per Visit', 'rn', 'Lead Origin_Landing Page Submission',
    'Last Activity_Email Opened', 'Specialization_Finance Management',
    'Specialization_Human Resource Management', 'Specialization_Marketing Management',
    'What is your current occupation_Unemployed', 'Tags_Other Tags',
    'Tags_Ringing', 'Tags_Will revert after reading the email', 'City_Mumbai',
    'City_Select', 'Last Notable Activity_Modified', 'Last Notable Activity_SMS Sent'
]

# Verificar y añadir la columna 'rn' si no existe
if 'rn' not in historical_data.columns:
    historical_data['rn'] = 0  # Asignar un valor por defecto si es necesario

# Seleccionar las características necesarias para el modelo
X = historical_data[columns_used_for_training]

# Generar predicciones con XGBoost
xgb_predictions = xgb_model.predict(X)
xgb_probabilities = xgb_model.predict_proba(X)[:, 1]  # Probabilidad de la clase 1

# Añadir las predicciones y las probabilidades al DataFrame histórico
historical_data["xgb_predictions"] = xgb_predictions
historical_data["xgb_probabilities"] = xgb_probabilities

# Guardar el DataFrame con predicciones y probabilidades en un CSV
historical_data.to_csv("final_historical_with_xgb_predictions.csv", index=False)

print("Predicciones y probabilidades guardadas en final_historical_with_xgb_predictions.csv")
