import pandas as pd
import pickle

# Cargar el modelo XGBoost
with open("C:/Users/DYLAN/Desktop/REPOS/MachineLearning/xgboost_model_final.pkl", "rb") as file:
    xgb_model = pickle.load(file)

# Cargar los datos históricos preparados
historical_data = pd.read_csv("C:/Users/DYLAN/Desktop/REPOS/MachineLearning/lead_scoring_TFG/datos_sinteticos/historico_preparado.csv")

# Lista de columnas utilizadas durante el entrenamiento del modelo XGBoost
columns_used_for_training = [
    'Lead Number', 'Total Time Spent on Website', 'Page Views Per Visit',
    'A free copy of Mastering The Interview', 'TotalVisits',
    'Average Time Per Visit', 'Last Activity_SMS Sent',
    'What is your current occupation_Unemployed',
    'What is your current occupation_Unknown',
    'What is your current occupation_Working Professional',
    'Tags_Already a student', 'Tags_Closed by Horizzon',
    'Tags_Interested in other courses', 'Tags_Other Tags',
    'Tags_Ringing', 'Tags_Unknown', 
    'Tags_Will revert after reading the email',
    'City_Mumbai', 'Last Notable Activity_Modified', 
    'Last Notable Activity_SMS Sent'
]

# Verificar que todas las columnas necesarias están presentes
missing_columns = [col for col in columns_used_for_training if col not in historical_data.columns]
for col in missing_columns:
    historical_data[col] = 0  # Asignar 0 por defecto si la columna falta

# Seleccionar las características necesarias para el modelo
X = historical_data[columns_used_for_training]

# Generar predicciones con XGBoost
xgb_predictions = xgb_model.predict(X)
xgb_probabilities = xgb_model.predict_proba(X)[:, 1]  # Probabilidad de la clase 1

# Añadir las predicciones y las probabilidades al DataFrame histórico
historical_data["xgb_predictions"] = xgb_predictions
historical_data["xgb_probabilities"] = xgb_probabilities

# Guardar el DataFrame con predicciones y probabilidades en un CSV
historical_data.to_csv("C:/Users/DYLAN/Desktop/REPOS/MachineLearning/final_historical_with_xgb_predictions.csv", index=False)

print("✅ Predicciones y probabilidades guardadas en 'final_historical_with_xgb_predictions.csv'")
