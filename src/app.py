from pickle import load
import streamlit as st
import numpy as np
import pandas as pd
from PIL import Image
from sklearn.preprocessing import StandardScaler

def home():
    st.title("When Your Body Sends Smoke Signals")
    st.subheader("Body Signals Smoking :no_smoking")
    st.write('''In today's era of scientific advancement, it's undeniable that cigarettes and tobacco pose grave risks to both smokers and those around them. Extensive research has revealed a wide range of health issues stemming from smoking, spanning from well-known cardiovascular and pulmonary problems to subtler influences on diabetes, renal function, liver health, and even sensory impairments like vision and hearing. Through the analysis of various health markers, we can pinpoint affected organs and gauge susceptibility to disease.

The "Body Signals of Smoking" project aims to harness bodily cues and biomarkers to predict smoking behaviors. By collecting comprehensive biomedical data, including metrics like hemoglobin levels, cholesterol concentrations, blood pressure readings, among others, we're training a machine learning model—a random forest classifier—to discern between smokers and non-smokers.

Our user-friendly application empowers individuals to input their own biomedical data with ease, allowing the model to swiftly classify their smoking status. This project is about early detection and intervention. By providing a powerful tool for identifying smoking behaviors, we're not only facilitating personal health awareness but also contributing to larger public health initiatives aimed at smoking prevention.
         ''')

    st.markdown("""
    <style>
        .main {
            background-color: #F7F7FF;
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
        h1 {
            text-align: center;
        }
        .centrado-con-margen {
            display: flex;
            justify-content: center;
            margin: 20px;
        }
    </style>
""", unsafe_allow_html=True)

    col1, _ = st.columns([2, 1])
    with col1:
        st.image(Image.open("body.jpg"), width=600)

   
# Página de gráficos informativos
def data():
    st.title("Here's an interesting fact:")
    # Primera fila de imágenes
    st.header("Did you know that")
    row1_col1, row1_col2 = st.columns(2)
    with row1_col1:
        st.image(Image.open("Gender_smoking.png"), width=300, caption="Men smoke more than women")
    with row1_col2:
        st.image(Image.open("hemoglobine_gender.png"), width=300, caption="Higher levels of hemoglobin are associated with smoking")
    
    # Segunda fila de imágenes
    row2_col1, row2_col2 = st.columns(2)
    with row2_col1:
        st.image(Image.open("GTP.png"), width=300, caption="Elevated levels of GTP (Guanosine triphosphate) are linked to smoking")
    with row2_col2:
        st.image(Image.open("Triglyceride.png"),width=300, caption="Elevated triglyceride levels are linked to tobacco consumption")


def prediction():
    st.title("Body-Signals-Smoking :no_smoking:")
    st.subheader("Introduce your data and analyze what your body signals reveal about smoking")
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

    # Cargar el modelo y el escalador
    try:
        model = load(open("/workspaces/Body_Signals_of_Smoking/src/random_forest_model_Default.pkl", "rb"))
        scaler = load(open("/workspaces/Body_Signals_of_Smoking/src/scaler.pkl", "rb"))
    except FileNotFoundError as e:
        st.error(f"Error: {e}. Please ensure random_forest_model_Default.pkl and scaler.pkl are in /workspaces/Final_Project_Body_Signals/")
        return

    # Clasificación de las etiquetas
    class_dict = {"0": "Non-Smoking", "1": "Smoking"}

    # Definir las variables numéricas
    num_variables = ['gender', 'Gtp', 'hemoglobin', 'height(cm)', 'triglyceride', 'waist(cm)', 'LDL', 'HDL',
                     'Cholesterol', 'ALT', 'fasting blood sugar', 'systolic', 'AST', 'relaxation', 'weight(kg)',
                     'age', 'serum creatinine', 'eyesight(left)', 'eyesight(right)', 'tartar', 'dental caries',
                     'Urine protein', 'hearing(left)', 'hearing(right)']

    # Rangos de las variables (ajustados según el dataset)
    variable_ranges = {
        'gender': (0, 1),
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
        'HDL': (20, 300),  
        'tartar': (0, 1),
        'dental caries': (0, 1),
        'hearing(left)': (1, 2),
        'hearing(right)': (1, 2),
        'Urine protein': (1, 4)
    }

    # Interfaz de usuario
    gender = st.selectbox("Gender", ["F", "M"])
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
    val18 = st.slider("Eyesight (Left)", min_value=0.0, max_value=2.0, step=0.1)
    val19 = st.slider("Eyesight (Right)", min_value=0.0, max_value=2.0, step=0.1)
    val20 = st.slider("Urine Protein", min_value=1.0, max_value=6.0, step=0.1)

    hearing_left = st.selectbox("Hearing (Left)", ["Normal", "Difficulty"])
    hearing_right = st.selectbox("Hearing (Right)", ["Normal", "Difficulty"])
    tartar = st.selectbox("Tartar", ["No", "Yes"])
    dental_caries = st.selectbox("Dental Caries", ["No", "Yes"])

    if st.button("Predict"):
        # Mapear valores
        gender_value = 1 if gender == "M" else 0
        hearing_left_value = 1 if hearing_left == "Normal" else 2
        hearing_right_value = 1 if hearing_right == "Normal" else 2
        tartar_value = 0 if tartar == "No" else 1
        dental_caries_value = 0 if dental_caries == "No" else 1

        # Crear DataFrame con los valores
        data = {
            "gender": [gender_value],
            "Gtp": [val2],
            "hemoglobin": [val3],
            "height(cm)": [val4],
            "triglyceride": [val5],
            "waist(cm)": [val6],
            "LDL": [val7],
            "HDL": [val8],
            "Cholesterol": [val9],
            "ALT": [val10],
            "fasting blood sugar": [val11],
            "systolic": [val12],
            "AST": [val13],
            "relaxation": [val14],
            "weight(kg)": [val15],
            "age": [val16],
            "serum creatinine": [val17],
            "eyesight(left)": [val18],
            "eyesight(right)": [val19],
            "tartar": [tartar_value],
            "dental caries": [dental_caries_value],
            "Urine protein": [val20],
            "hearing(left)": [hearing_left_value],
            "hearing(right)": [hearing_right_value]
        }
        df_scaled = pd.DataFrame(data, columns=num_variables)

        # Escalar los datos
        try:
            data_normalized = scaler.transform(df_scaled)
            prediction = model.predict(data_normalized)[0]
            st.write("Prediction:", class_dict[str(prediction)])
        except Exception as e:
            st.error(f"Error during prediction: {e}")

def Limitations_Future_Improvement():
    st.title("Limitations and Future Improvement")
    st.write('''Some limitations of the dataset that may affect the prediction of our models include:

1. Lack of information regarding the time period for sample collection.
2. Absence of details regarding the country or city from which the data originates.
             
It would be beneficial to include these two pieces of information to facilitate the integration of other demographic data.
             
To enhance the dataset:
1. Include demographic variables (e.g., education, income) and physiological indicators (like exhaled CO levels) to gauge tobacco's impact.
2. Integrate behavioral data (e.g., smoking habits, quit attempts) for a comprehensive view.
3. Consider cultural influences on smoking behavior and health outcomes.
4. Account for environmental factors (e.g., air quality, proximity to pollutants) in risk assessment.
5. Incorporate user feedback for iterative model enhancement and user interface optimization.
         '''
    )

def main():
    # Custom CSS to inject into the Streamlit app
    st.markdown("""
    <style>
    /* Change the sidebar background color */
    .css-1d391kg {
        background-color: #FFA07A !important;
    }
    /* Change the sidebar text color */
    .css-1aumxhk {
        color: #FFD700 !important;
    }
    </style>
    """, unsafe_allow_html=True)

    st.sidebar.title("Menu")
    selection = st.sidebar.radio("Go to", ["Home", "Relevant Data", "Prediction", "Limitations and Future Improvement"])

    if selection == "Home":
        home()
    elif selection == "Relevant Data":
        data()
    elif selection == "Prediction":
        prediction()
    elif selection == "Limitations and Future Improvement":
        Limitations_Future_Improvement()

if __name__ == "__main__":
    main()