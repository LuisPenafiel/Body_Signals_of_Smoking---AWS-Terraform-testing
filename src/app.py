import os
import boto3
from pickle import load
import streamlit as st
import numpy as np
import pandas as pd
from PIL import Image
from sklearn.preprocessing import StandardScaler
import mysql.connector
import sqlite3
from datetime import datetime

# --- Environment Detection ---
IS_AWS = 'AWS_REGION' in os.environ or 'AWS_LAMBDA_FUNCTION_NAME' in os.environ
IS_LAMBDA = 'AWS_LAMBDA_FUNCTION_NAME' in os.environ

# --- S3 and File Configuration ---
BUCKET_NAME = 'smoking-body-signals-data-dev'
REGION_NAME = 'eu-central-1'
if IS_AWS:
    s3 = boto3.client('s3', region_name=REGION_NAME)
    BASE_PATH = '/tmp'
else:
    BASE_PATH = '/workspaces/Body_Signals_of_Smoking---AWS-Terraform-testing/src'

# File paths with caching
@st.cache_data
def get_file_paths():
    return {
        'model': os.path.join(BASE_PATH, 'random_forest_model_Default.pkl'),
        'scaler': os.path.join(BASE_PATH, 'scaler.pkl'),
        'body_image': os.path.join(BASE_PATH, 'body.jpg'),
        'gender_smoke': os.path.join(BASE_PATH, 'Gender_smoking.png'),
        'gtp': os.path.join(BASE_PATH, 'GTP.png'),
        'hemo': os.path.join(BASE_PATH, 'hemoglobine_gender.png'),
        'trigly': os.path.join(BASE_PATH, 'Triglyceride.png')
    }

paths = get_file_paths()

# --- Ensure Files Are Available ---
def ensure_files():
    try:
        if IS_AWS and not IS_LAMBDA:
            for key, s3_key in [('model', 'src/random_forest_model_Default.pkl'),
                                ('scaler', 'src/scaler.pkl'),
                                ('body_image', 'src/body.jpg'),
                                ('gender_smoke', 'src/Gender_smoking.png'),
                                ('gtp', 'src/GTP.png'),
                                ('hemo', 'src/hemoglobine_gender.png'),
                                ('trigly', 'src/Triglyceride.png')]:
                local_path = paths[key]
                if not os.path.exists(local_path):
                    s3.download_file(BUCKET_NAME, s3_key, local_path)
                    st.success(f"Downloaded {s3_key} from S3.")
        else:
            for key, local_path in paths.items():
                if not os.path.exists(local_path):
                    st.error(f"File not found: {local_path}. Place it in {BASE_PATH}.")
                    st.stop()
    except Exception as e:
        st.error(f"File handling error: {e}")
        st.experimental_rerun()  # Reinicia si hay fallo de loop

# --- Database Manager Class ---
class DatabaseManager:
    def __init__(self):
        self.conn = None
        self._init_connection()

    def _init_connection(self):
        if IS_AWS:
            config = {
                'host': os.environ.get('RDS_HOST', 'your-rds-endpoint.eu-central-1.rds.amazonaws.com'),
                'user': os.environ.get('RDS_USER', 'admin'),
                'password': os.environ.get('RDS_PASSWORD', 'yourpassword'),
                'database': os.environ.get('RDS_DB', 'smoking_db')
            }
            try:
                self.conn = mysql.connector.connect(**config)
                cursor = self.conn.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS predictions (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        gender VARCHAR(10),
                        hemoglobin FLOAT,
                        prediction VARCHAR(20),
                        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        INDEX idx_gender (gender)
                    )
                """)
                self.conn.commit()
            except mysql.connector.Error as e:
                st.error(f"Error connecting to RDS: {e}")
                st.stop()
        else:
            db_path = '/workspaces/Body_Signals_of_Smoking/data/smoking_db.sqlite'
            try:
                self.conn = sqlite3.connect(db_path)
                cursor = self.conn.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS predictions (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        gender TEXT,
                        hemoglobin REAL,
                        prediction TEXT,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                self.conn.commit()
            except sqlite3.Error as e:
                st.error(f"Error connecting to SQLite: {e}")
                st.stop()

    def save_prediction(self, gender, hemoglobin, prediction):
        try:
            cursor = self.conn.cursor()
            if IS_AWS:
                cursor.execute(
                    "INSERT INTO predictions (gender, hemoglobin, prediction) VALUES (%s, %s, %s)",
                    (gender, hemoglobin, prediction)
                )
            else:
                cursor.execute(
                    "INSERT INTO predictions (gender, hemoglobin, prediction) VALUES (?, ?, ?)",
                    (gender, hemoglobin, prediction)
                )
            self.conn.commit()
        except (mysql.connector.Error, sqlite3.Error) as e:
            st.error(f"Error saving prediction: {e}")

    def close(self):
        if self.conn:
            self.conn.close()

# --- Load Model and Scaler with Cache ---
@st.cache_data
def load_model_and_scaler(model_path, scaler_path):
    try:
        with open(model_path, 'rb') as f:
            model = load(f)
        with open(scaler_path, 'rb') as f:
            scaler = load(f)
        return model, scaler
    except FileNotFoundError as e:
        st.error(f"Error loading model or scaler: {e}")
        st.stop()

# --- Sections ---
def home():
    st.markdown("<div class='header'><h1><i class='fas fa-lungs'></i> Body Signals of Smoking</h1><p class='slogan animate__animated animate__fadeIn'>Empowering Health Awareness</p></div>", unsafe_allow_html=True)
    st.markdown("""
        <style>
            .content-text {
                font-family: 'Roboto', sans-serif;
                font-weight: bold;
                color: #2C3E50;
                line-height: 1.6;
            }
        </style>
    """, unsafe_allow_html=True)
    st.markdown("""
        <div class='content-text'>
            In today's era of scientific advancement, it is undeniable that cigarettes and tobacco pose serious risks to both smokers and those around them. Extensive research has revealed a wide range of health issues stemming from smoking, from well-known cardiovascular and pulmonary diseases to more subtle influences on diabetes, kidney function, liver health, and even sensory impairments such as vision and hearing. By analyzing various health markers, we can identify affected organs and assess susceptibility to diseases.

            The "Body Signals of Smoking" project leverages bodily signals and biomarkers to predict smoking behaviors. Using comprehensive biomedical data—such as hemoglobin levels, cholesterol concentrations, and blood pressure readings—we train a random forest classifier to distinguish between smokers and non-smokers.

            Our user-friendly application allows individuals to input their biomedical data for quick smoking status classification. This project focuses on early detection and intervention, fostering personal health awareness and supporting public health initiatives aimed at smoking prevention.
        </div>
    """, unsafe_allow_html=True)
    col1, col2 = st.columns([2, 1])
    with col1:
        try:
            st.image(Image.open(paths['body_image']), caption="Body Health Overview", use_container_width=True)
        except FileNotFoundError:
            st.error("Image 'body.jpg' not found.")

def data():
    st.header("Relevant Data Insights")
    st.subheader("Did You Know?")
    cols = st.columns(2)
    with cols[0]:
        try:
            st.image(Image.open(paths['gender_smoke']), caption="Men Smoke More Than Women", use_container_width=True)
        except FileNotFoundError:
            st.error("Image 'Gender_smoking.png' not found.")
    with cols[1]:
        try:
            st.image(Image.open(paths['hemo']), caption="Higher Hemoglobin Linked to Smoking", use_container_width=True)
        except FileNotFoundError:
            st.error("Image 'hemoglobine_gender.png' not found.")
    cols = st.columns(2)
    with cols[0]:
        try:
            st.image(Image.open(paths['gtp']), caption="Elevated GTP and Smoking", use_container_width=True)
        except FileNotFoundError:
            st.error("Image 'GTP.png' not found.")
    with cols[1]:
        try:
            st.image(Image.open(paths['trigly']), caption="Triglycerides and Tobacco Use", use_container_width=True)
        except FileNotFoundError:
            st.error("Image 'Triglyceride.png' not found.")

def prediction(db):
    st.header("Smoking Prediction :no_smoking:")
    st.subheader("Enter Your Data for Analysis")
    st.markdown('<div class="medical-badge">PATIENT ASSESSMENT</div>', unsafe_allow_html=True)
    
    with st.container():
        st.write("Enter patient biomarkers for smoking status prediction:")
        
        ensure_files()
        model, scaler = load_model_and_scaler(paths['model'], paths['scaler'])

        class_dict = {"0": "Non-Smoker", "1": "Smoker"}
        num_variables = ['gender', 'Gtp', 'hemoglobin', 'height(cm)', 'triglyceride', 'waist(cm)', 'LDL', 'HDL',
                         'Cholesterol', 'ALT', 'fasting blood sugar', 'systolic', 'AST', 'relaxation', 'weight(kg)',
                         'age', 'serum creatinine', 'eyesight(left)', 'eyesight(right)', 'tartar', 'dental caries',
                         'Urine protein', 'hearing(left)', 'hearing(right)']

        with st.form(key='prediction_form'):
            col1, col2 = st.columns(2)
            with col1:
                gender = st.selectbox("Gender", ["F", "M"], help="Select your gender")
                val2 = st.slider("Gtp", min_value=1.0, max_value=996.0, step=0.1, value=100.0)
                val3 = st.slider("Hemoglobin", min_value=7.4, max_value=18.7, step=0.1, value=12.0)
                val4 = st.slider("Height (cm)", min_value=100.0, max_value=230.0, step=0.1, value=170.0)
            with col2:
                val5 = st.slider("Triglycerides", min_value=31.0, max_value=1029.0, step=0.1, value=150.0)
                val6 = st.slider("Waist (cm)", min_value=80.0, max_value=102.0, step=0.1, value=90.0)
                val7 = st.slider("LDL", min_value=70.0, max_value=300.0, step=0.1, value=100.0)
            with col1:
                val8 = st.slider("HDL", min_value=20.0, max_value=300.0, step=0.1, value=50.0)
                val9 = st.slider("Cholesterol", min_value=300.0, max_value=700.0, step=0.1, value=200.0)
                val10 = st.slider("ALT", min_value=1.0, max_value=996.0, step=0.1, value=20.0)
            with col2:
                val11 = st.slider("Fasting Blood Sugar", min_value=0.0, max_value=126.0, step=0.1, value=90.0)
                val12 = st.slider("Systolic", min_value=0.0, max_value=140.0, step=0.1, value=120.0)
                val13 = st.slider("AST", min_value=10.0, max_value=1543.0, step=0.1, value=25.0)
            with col1:
                val14 = st.slider("Relaxation", min_value=0.0, max_value=120.0, step=0.1, value=80.0)
                val15 = st.slider("Weight (kg)", min_value=35.0, max_value=300.0, step=0.1, value=70.0)
                val16 = st.slider("Age", min_value=0.0, max_value=100.0, step=0.1, value=30.0)
            with col2:
                val17 = st.slider("Serum Creatinine", min_value=0.27, max_value=6.81, step=0.01, value=1.0)
                val18 = st.slider("Eyesight (Left)", min_value=0.0, max_value=2.0, step=0.1, value=1.0)
                val19 = st.slider("Eyesight (Right)", min_value=0.0, max_value=2.0, step=0.1, value=1.0)
                val20 = st.slider("Urine Protein", min_value=1.0, max_value=6.0, step=0.1, value=1.0)

            hearing_left = st.selectbox("Hearing (Left)", ["Normal", "Difficulty"])
            hearing_right = st.selectbox("Hearing (Right)", ["Normal", "Difficulty"])
            tartar = st.selectbox("Tartar", ["No", "Yes"])
            dental_caries = st.selectbox("Dental Caries", ["No", "Yes"])

            if st.form_submit_button("Predict", help="Get your smoking prediction"):
                gender_value = 1 if gender == "M" else 0
                hearing_left_value = 1 if hearing_left == "Normal" else 2
                hearing_right_value = 1 if hearing_right == "Normal" else 2
                tartar_value = 0 if tartar == "No" else 1
                dental_caries_value = 0 if dental_caries == "No" else 1

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

                try:
                    # Ajuste para coincidir con nombres de características del modelo
                    if hasattr(model, 'feature_names_in_'):
                        if not all(col in model.feature_names_in_ for col in df_scaled.columns):
                            st.warning("Feature names may not match the trained model. Please verify training data in your notebook.")
                    data_normalized = scaler.transform(df_scaled)
                    prediction_result = model.predict(data_normalized)[0]
                    result_text = class_dict[str(prediction_result)]
                    st.success(f"Prediction: **{result_text}**", icon="✅")
                    db.save_prediction(gender, val3, result_text)
                    st.session_state.predictions = st.session_state.get('predictions', 0) + 1
                    st.metric("Total Predictions", st.session_state.predictions)
                except Exception as e:
                    st.error(f"Prediction Error: {e}")

def limitations_future_improvement():
    st.header("Research Insights")
    st.markdown('<div class="research-badge">FUTURE HORIZONS</div>', unsafe_allow_html=True)
    with st.container():
        st.markdown("""
            <style>
                .insight-panel {
                    background: linear-gradient(135deg, #E3F2FD, #F5F7FA);
                    padding: 20px;
                    border-radius: 15px;
                    margin-bottom: 20px;
                    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
                    transition: transform 0.3s ease, box-shadow 0.3s ease;
                }
                .insight-panel:hover {
                    transform: translateY(-5px);
                    box-shadow: 0 6px 15px rgba(0, 0, 0, 0.2);
                }
                .limitation-icon { color: #FF5722; font-size: 1.5rem; }
                .improvement-icon { color: #4CAF50; font-size: 1.5rem; }
                .content-text {
                    font-family: 'Roboto', sans-serif;
                    font-size: 1.1rem;
                    color: #333;
                    line-height: 1.8;
                }
                .progress-container {
                    height: 8px;
                    background: #CFD8DC;
                    border-radius: 4px;
                    margin-top: 10px;
                }
                .progress-bar {
                    height: 100%;
                    background: linear-gradient(90deg, #4CAF50, #2196F3);
                    border-radius: 4px;
                    width: 40%; /* Ajustable */
                    transition: width 1s ease;
                }
            </style>
        """, unsafe_allow_html=True)

        st.markdown("""
            <div class='insight-panel'>
                <h3><i class='limitation-icon fas fa-exclamation-triangle'></i> Current Challenges</h3>
                <div class='content-text'>
                    - Historical data lacks time-specific context.  
                    - No geographic data for environmental impact.  
                    - Missing details on smoking intensity.  
                    - Limited socioeconomic and behavioral insights.
                </div>
                <div class='progress-container'><div class='progress-bar' style='width: 30%;'></div></div>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("""
            <div class='insight-panel'>
                <h3><i class='improvement-icon fas fa-rocket'></i> Future Directions</h3>
                <div class='content-text'>
                    - Conducting live validation studies.  
                    - Implementing CO breath analysis.  
                    - Mapping environmental risk factors.  
                    - Adding behavioral health tracking.  
                    - Tailoring for cultural diversity.  
                    - Enhancing with AI clinical tools.
                </div>
                <div class='progress-container'><div class='progress-bar' style='width: 20%;'></div></div>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("""
            <div style='background: #FFE0B2; padding: 15px; border-radius: 10px; text-align: center; margin-top: 20px;'>
                <p style='color: #EF6C00; font-weight: bold;'>
                    <i class='fas fa-shield-alt'></i> For research use only. Seek professional medical advice for health decisions.
                </p>
            </div>
        """, unsafe_allow_html=True)

# --- Main Function ---
def main():
    st.set_page_config(page_title="Body Signals of Smoking", layout="wide", initial_sidebar_state="expanded")
    st.markdown("""
        <link href="https://fonts.googleapis.com/css2?family=Roboto&display=swap" rel="stylesheet">
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.6.0/css/all.min.css" rel="stylesheet">
        <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
        <style>
            .header {
                background: linear-gradient(90deg, #2ECC71 0%, #3498DB 100%);
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                margin-bottom: 20px;
            }
            .header h1 {
                color: white;
                font-size: 2.5rem;
                font-family: 'Roboto', sans-serif;
                text-align: center;
                margin: 0;
            }
            .header .slogan {
                color: #ECF0F1;
                font-size: 1.2rem;
                text-align: center;
                margin-top: 5px;
            }
            .main {
                background-color: #F5F7FA;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            }
            .stSidebar {
                background: linear-gradient(180deg, #2ECC71, #3498DB); /* Verde azulado */
                padding: 20px;
                color: white;
            }
            .stSidebar .sidebar-content {
                padding: 0;
            }
            .stSidebar h2 {
                color: white;
                font-size: 1.5rem;
                margin-bottom: 20px;
                text-align: center;
            }
            .stSidebar .stRadio > label {
                color: white !important;
                font-size: 1.1rem;
                font-family: 'Roboto', sans-serif;
                font-weight: 700;
                padding: 5px 0;
                transition: color 0.3s;
            }
            .stSidebar .stRadio > label:hover {
                color: #FFEB3B !important; /* Amarillo claro al hover */
            }
            .medical-badge {
                background-color: #2ECC71;
                color: white;
                padding: 5px 10px;
                border-radius: 5px;
                display: inline-block;
                font-weight: bold;
            }
            .research-badge {
                background-color: #3498DB;
                color: white;
                padding: 5px 10px;
                border-radius: 5px;
                display: inline-block;
                font-weight: bold;
            }
            .stButton>button {
                background: linear-gradient(90deg, #27AE60, #2ECC71);
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 8px;
                font-size: 16px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                transition: all 0.3s ease;
            }
            .stButton>button:hover {
                background: linear-gradient(90deg, #219653, #27AE60);
                transform: translateY(-2px);
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            }
            .stSuccess {
                background-color: #2ECC71;
                color: white;
                padding: 10px;
                border-radius: 5px;
                text-align: center;
                font-weight: bold;
            }
            .stError {
                background-color: #E74C3C;
                color: white;
                padding: 10px;
                border-radius: 5px;
                text-align: center;
            }
            @media (max-width: 600px) {
                .header h1 { font-size: 1.8rem; }
                .header .slogan { font-size: 1rem; }
                .stButton>button { padding: 10px 20px; font-size: 14px; }
            }
        </style>
    """, unsafe_allow_html=True)

    st.sidebar.title("Menu")
    selection = st.sidebar.radio("Navigation", ["Home", "Relevant Data", "Prediction", "Limitations"], label_visibility="collapsed")

    ensure_files()
    db = DatabaseManager()

    if selection == "Home":
        home()
    elif selection == "Relevant Data":
        data()
    elif selection == "Prediction":
        prediction(db)
    elif selection == "Limitations":
        limitations_future_improvement()

    db.close()

if __name__ == "__main__":
    main()