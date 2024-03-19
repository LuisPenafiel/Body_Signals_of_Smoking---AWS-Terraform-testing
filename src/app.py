# Voy a poner como yo hice lo mio con Streamlit ya iremos cambiando y mezclando ambos
# Aqui esta todo lo que podemos usar https://docs.streamlit.io/library/api-reference    https://www.youtube.com/watch?v=D0D4Pa22iG0&t=1s

from pickle import load
import streamlit as st
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler

# Página de inicio
def home():
    st.title("Body-Signals-Smoking :no_smoking:")
    st.subheader("Visualiza y analiza datos relacionados con el tabaquismo")
    st.write('''
         Está demostrado científicamente que el cigarrillo/tabaco es perjudicial para la salud tanto de las personas fumadoras como las personas que se consideran fumadoras pasivas. Se ha demostrado que a consecuencia de fumar se producen una serie de enfermedades y trastornos en todo el cuerpo, algunas más conocidas que otras, pero que abarcan desde problemas cardiovasculares, pulmonares, influencia sobre la diabetes, riñones, hígado, piel como también afectan la vista, los oídos y la boca, entre otros. A través de distintas variables de salud (que podemos llamar marcadores) se puede detectar qué órganos están afectados o qué riesgo de enfermedades.

Usando un modelo de aprendizaje supervisado o "machine learning" se predice si una persona es fumadora o no a través de distintas señales que muestra el cuerpo.
         '''
         )

# Página de predicción
def prediction():
    st.title("Prediction Page")

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
        'gender': (0, 1),  # Assuming gender is coded as 0 and 1
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
    # Crear un DataFrame con nombres de columnas para el escalado
    df_scaled = pd.DataFrame(data=np.zeros((1, len(num_variables))), columns=num_variables)

    # Inicializar el escalador
    scaler = StandardScaler()
    scaler.fit(df[num_variables])

    # Título de la aplicación
    st.title("Body-Signals-Smoking :no_smoking:")
    st.subheader("Visualiza y analiza datos relacionados con el tabaquismo")
    st.markdown("""
        <style>
            .main {
                background-color: #F0F0F0;
            }
            .stButton>button {
                color: white;
                background-color: #4CAF50;
                border: none;
                padding: 14px 28px;
                cursor: pointer;
                border-radius: 8px;
            }
            .stButton>button:hover {
                background-color: #45A049;
            }
            .highlight:hover {
                background-color: #FFCCCB;
                transition: background-color 0.5s ease;
            }
        </style>
    """, unsafe_allow_html=True)

    # Crear un selectbox para el género
    gender = st.selectbox("Gender", ["F", "M"])

    # Crear sliders para las otras variables
    val2 = st.slider("Gtp", min_value=1.0, max_value=996.0, step=0.1)
    val3 = st.slider("Hemoglobin", min_value=7.4, max_value=18.7, step=0.1)
    val4 = st.slider("Height(cm)", min_value=100.0, max_value=230.0, step=0.1)
    val5 = st.slider("Triglyceride", min_value=31.0, max_value=1029.0, step=0.1)
    val6 = st.slider("Waist(cm)", min_value=80.0, max_value=102.0, step=0.1)
    val7 = st.slider("LDL", min_value=70.0, max_value=300.0, step=0.1)
    val8 = st.slider("HDL", min_value=20.0, max_value=300.0, step=0.1)
    val9 = st.slider("Cholesterol", min_value=300.0, max_value=700.0, step=0.1)
    val10 = st.slider("ALT", min_value=1.0, max_value=996.0, step=0.1)
    val11 = st.slider("Fasting Blood Sugar", min_value=0.0, max_value=126.0, step=0.1)
    val12 = st.slider("Systolic", min_value=0.0, max_value=140.0, step=0.1)
    val13 = st.slider("AST", min_value=10.0, max_value=1543.0, step=0.1)
    val14 = st.slider("Relaxation", min_value=0.0, max_value=120.0, step=0.1)
    val15 = st.slider("Weight(kg)", min_value=35.0, max_value=300.0, step=0.1)
    val16 = st.slider("Age", min_value=0.0, max_value=100.0, step=0.1)
    val17 = st.slider("Serum Creatinine", min_value=0.27, max_value=6.81, step=0.01)
    val18 = st.slider("Eyesight (Left)", min_value=0, max_value=2)
    val19 = st.slider("Eyesight (Right)", min_value=0, max_value=2)
    val20 = st.slider("Tartar", min_value=0, max_value=1)
    val21 = st.slider("Dental Caries", min_value=0, max_value=1)
    val22 = st.slider("Urine Protein", min_value=0, max_value=1)
    val23 = st.slider("Hearing (Left)", min_value=0, max_value=1)
    val24 = st.slider("Hearing (Right)", min_value=0, max_value=1)

    # Botón para realizar la predicción
    if st.button("Predict"):
        # Mapear el género a 0 o 1
        gender_value = 1 if gender == "M" else 0
        # Crear un DataFrame con los valores de los sliders
        data = {
            "gender": gender_value,
            "Gtp": val2,
            "hemoglobin": val3,
            "height(cm)": val4,
            "triglyceride": val5,
            "waist(cm)": val6,
            "LDL": val7,
            "HDL": val8,
            "Cholesterol": val9,
            "ALT": val10,
            "fasting blood sugar": val11,
            "systolic": val12,
            "AST": val13,
            "relaxation": val14,
            "weight(kg)": val15,
            "age": val16,
            "serum creatinine": val17,
            "eyesight(left)": val18,
            "eyesight(right)": val19,
            "tartar": val20,
            "dental caries": val21,
            "Urine protein": val22,
            "hearing(left)": val23,
            "hearing(right)": val24
        }
        # Crear un DataFrame a partir de los valores y escalarlos
        df_scaled = pd.DataFrame(data=[data])
        data_normalized = scaler.transform(df_scaled)
        # Realizar la predicción
        prediction = model.predict(data_normalized)[0]
        # Mostrar el resultado de la predicción
        st.write("Prediction:", class_dict[str(prediction)])

def data_visualization():
    st.title("Data Visualization Page")
    # Tu código para la página de visualización de datos va aquí

# Función principal para manejar la navegación entre páginas
def main():
    st.sidebar.title("Menu")
    selection = st.sidebar.radio("Go to", ["Home", "Prediction", "Data Visualization"])

    if selection == "Home":
        home()
    elif selection == "Prediction":
        prediction()
    elif selection == "Data Visualization":
        data_visualization()

if __name__ == "__main__":
    main()
 


