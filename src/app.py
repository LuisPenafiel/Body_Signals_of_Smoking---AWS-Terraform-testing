# Aqui esta todo lo que podemos usar https://docs.streamlit.io/library/api-reference    https://www.youtube.com/watch?v=D0D4Pa22iG0&t=1s

from pickle import load
import streamlit as st
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler

# Cargar el modelo
model = load(open("/workspaces/Final_Project_Body_Signals/models/random_forest_model_Default.pkl", "rb"))

# Clasificación de las etiquetas
class_dict = {
    "0": "Non-Smoking",
    "1": "Smoking",
}

# Leer los datos
df = pd.read_csv("/workspaces/Final_Project_Body_Signals/data/processed/total_data_c2.csv")

# Definir las variables numéricas
num_variables = ['gender', 'Gtp', 'hemoglobin', 'height(cm)', 'triglyceride', 'waist(cm)', 'LDL', 'HDL',
                 'Cholesterol', 'ALT', 'fasting blood sugar', 'systolic', 'AST', 'relaxation', 'weight(kg)',
                 'age', 'serum creatinine', 'eyesight(left)', 'eyesight(right)', 'tartar', 'dental caries',
                 'Urine protein', 'hearing(left)', 'hearing(right)']

# Rangos de las variables
variable_ranges = {
    'hemoglobin': (7.4, 18.7),
    'height(cm)': (100, 230),
    'weight(kg)': (35, 300),
    'triglyceride': (31, 1029),
    'Gtp': (1, 996),
    'waist(cm)': (80, 102),
    'serum creatinine': (0.27, 6.81),
    'relaxation': (0, 120),
    'fasting blood sugar': (0, 126),
    'ALT': (1, 996),
    'systolic': (0, 140),
    'eyesight(right)': (0, 2),
    'eyesight(left)': (0, 2),
    'AST': (10, 1543),
    'Cholesterol': (300, 700),
    'LDL': (70, 300),
    'age': (0, 100),
    'HDL': (20, 300)
}

# Inicializar el escalador
scaler = StandardScaler()
scaler.fit(df[num_variables])

# Título de la aplicación
st.title("Body-Signals-Smoking")

# Crear sliders para cada variable
for i, variable in enumerate(num_variables, start=1):
    # Obtener los valores mínimo y máximo de la columna
    min_value, max_value = df[variable].min(), df[variable].max()
    # Crear el slider con una clave única
    slider_key = f"slider_{i}_{variable}"
    st.slider(f"val{i} = {variable.capitalize()}", min_value, max_value, key=slider_key)

# Botón para realizar la predicción
if st.button("Predict"):
    # Recoger los valores de los sliders
    slider_values = [st.session_state[f"slider_{i}_{variable}"] for i, variable in enumerate(num_variables, start=1)]
    # Normalizar los datos
    data_normalized = scaler.transform([slider_values])
    # Realizar la predicción
    prediction = model.predict(data_normalized)[0]
    # Mostrar el resultado de la predicción
    st.write("Prediction:", class_dict[str(prediction)])


    ############################chat me ideas que podemos anadir en el codigo para hacer mas vistoso##############


