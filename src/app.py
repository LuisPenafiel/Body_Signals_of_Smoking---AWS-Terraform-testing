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

# --- Environment Detection ---
# Check if we are on AWS by looking for the AWS_REGION environment variable
IS_AWS = 'AWS_REGION' in os.environ

# --- S3 Configuration (only for AWS) ---
if IS_AWS:
    BUCKET_NAME = 'smoking-body-signals-data-dev'
    REGION_NAME = 'eu-central-1'
    s3 = boto3.client('s3', region_name=REGION_NAME)

# --- File Paths ---
if IS_AWS:
    BASE_PATH = '/tmp'  # On AWS, use /tmp for temporary files
else:
    BASE_PATH = '/workspaces/Body_Signals_of_Smoking/src'  # On Codespaces, use local paths

MODEL_PATH = os.path.join(BASE_PATH, 'random_forest_model_Default.pkl')
SCALER_PATH = os.path.join(BASE_PATH, 'scaler.pkl')
BODY_IMAGE_PATH = os.path.join(BASE_PATH, 'body.jpg')
GENDER_SMOKE_PATH = os.path.join(BASE_PATH, 'Gender_smoking.png')
GTP_PATH = os.path.join(BASE_PATH, 'GTP.png')
HEMO_PATH = os.path.join(BASE_PATH, 'hemoglobine_gender.png')
TRIGLY_PATH = os.path.join(BASE_PATH, 'Triglyceride.png')

# --- Function to Download Files from S3 (only on AWS) ---
def download_s3_files():
    if not IS_AWS:  # Si no estamos en AWS, no intentamos descargar
        return
    try:
        s3.download_file(BUCKET_NAME, 'src/random_forest_model_Default.pkl', MODEL_PATH)
        s3.download_file(BUCKET_NAME, 'src/scaler.pkl', SCALER_PATH)
        s3.download_file(BUCKET_NAME, 'src/body.jpg', BODY_IMAGE_PATH)
        s3.download_file(BUCKET_NAME, 'src/Gender_smoking.png', GENDER_SMOKE_PATH)
        s3.download_file(BUCKET_NAME, 'src/GTP.png', GTP_PATH)
        s3.download_file(BUCKET_NAME, 'src/hemoglobine_gender.png', HEMO_PATH)
        s3.download_file(BUCKET_NAME, 'src/Triglyceride.png', TRIGLY_PATH)
        st.success("Archivos descargados exitosamente desde S3.")
    except Exception as e:
        st.error(f"Error al descargar archivos desde S3: {e}")
        st.stop()

# --- Database Configuration ---
if IS_AWS:
    # On AWS, use RDS MySQL (update with your RDS credentials)
    DB_CONFIG = {
        'host': 'your-rds-endpoint.eu-central-1.rds.amazonaws.com',
        'user': 'admin',
        'password': 'yourpassword',
        'database': 'smoking_db'
    }
    def init_db():
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS predictions (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    gender VARCHAR(10),
                    hemoglobin FLOAT,
                    prediction VARCHAR(20),
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()
            return conn
        except mysql.connector.Error as e:
            st.error(f"Error connecting to MySQL: {e}")
            st.stop()
else:
    # On Codespaces, use SQLite
    DB_PATH = '/workspaces/Body_Signals_of_Smoking/data/smoking_db.sqlite'
    def init_db():
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS predictions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    gender TEXT,
                    hemoglobin REAL,
                    prediction TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()
            return conn
        except sqlite3.Error as e:
            st.error(f"Error connecting to SQLite: {e}")
            st.stop()

# --- Function to Save Prediction ---
def save_prediction(gender, hemoglobin, prediction, conn):
    try:
        cursor = conn.cursor()
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
        conn.commit()
    except (mysql.connector.Error, sqlite3.Error) as e:
        st.error(f"Error saving to database: {e}")

# --- Home Section ---
def home():
    st.title("When Your Body Sends Smoke Signals")
    st.subheader("Body Signals of Smoking :no_smoking")
    st.write('''In today's era of scientific advancement, it is undeniable that cigarettes and tobacco pose serious risks to both smokers and those around them. Extensive research has revealed a wide range of health issues stemming from smoking, from well-known cardiovascular and pulmonary diseases to more subtle influences on diabetes, kidney function, liver health, and even sensory impairments such as vision and hearing. By analyzing various health markers, we can identify affected organs and assess susceptibility to diseases.

The "Body Signals of Smoking" project aims to leverage bodily signals and biomarkers to predict smoking behaviors. By collecting comprehensive biomedical data, such as hemoglobin levels, cholesterol concentrations, blood pressure readings, among others, we are training a machine learning model—a random forest classifier—to distinguish between smokers and non-smokers.

Our user-friendly application allows individuals to easily input their own biomedical data, enabling the model to quickly classify their smoking status. This project is about early detection and intervention. By providing a powerful tool to identify smoking behaviors, we not only facilitate personal health awareness but also contribute to broader public health initiatives aimed at smoking prevention.
         ''')
    st.markdown("""
    <style>
        .main { background-color: #F7F7FF; }
        .stButton>button {
            color: white;
            background-color: #4CAF50;
            border: none;
            padding: 14px 28px;
            cursor: pointer;
            border-radius: 8px;
        }
        .stButton>button:hover { background-color: #45A049; }
        h1 { text-align: center; }
    </style>
    """, unsafe_allow_html=True)
    col1, _ = st.columns([2, 1])
    with col1:
        try:
            st.image(Image.open(BODY_IMAGE_PATH), width=600)
        except FileNotFoundError:
            st.error("Image 'body.jpg' not found. Ensure it is in the correct path.")

# --- Data Section ---
def data():
    st.title("Here's an interesting fact:")
    st.header("Did you know that")
    row1_col1, row1_col2 = st.columns(2)
    with row1_col1:
        try:
            st.image(Image.open(GENDER_SMOKE_PATH), width=300, caption="Men smoke more than women")
        except FileNotFoundError:
            st.error("Image 'Gender_smoking.png' not found.")
    with row1_col2:
        try:
            st.image(Image.open(HEMO_PATH), width=300, caption="Higher levels of hemoglobin are associated with smoking")
        except FileNotFoundError:
            st.error("Image 'hemoglobine_gender.png' not found.")
    
    row2_col1, row2_col2 = st.columns(2)
    with row2_col1:
        try:
            st.image(Image.open(GTP_PATH), width=300, caption="Elevated levels of GTP are linked to smoking")
        except FileNotFoundError:
            st.error("Image 'GTP.png' not found.")
    with row2_col2:
        try:
            st.image(Image.open(TRIGLY_PATH), width=300, caption="Elevated triglyceride levels are related to tobacco consumption")
        except FileNotFoundError:
            st.error("Image 'Triglyceride.png' not found.")

# --- Prediction Section ---
def prediction(conn):
    st.title("Body-Signals-Smoking :no_smoking:")
    st.subheader("Enter your data and analyze what your body signals reveal about smoking")
    st.markdown("""
        <style>
            .main { background-color: #F0F0F0; }
            .stButton>button {
                color: white;
                background-color: #4CAF50;
                border: none;
                padding: 14px 28px;
                cursor: pointer;
                border-radius: 8px;
            }
            .stButton>button:hover { background-color: #45A049; }
        </style>
    """, unsafe_allow_html=True)

    # Load the model and scaler
    try:
        model = load(open(MODEL_PATH, "rb"))
        scaler = load(open(SCALER_PATH, "rb"))
    except FileNotFoundError as e:
        st.error(f"Error: {e}. Ensure the model and scaler are available.")
        return

    # Label classification
    class_dict = {"0": "Non-Smoker", "1": "Smoker"}

    # Define numerical variables
    num_variables = ['gender', 'Gtp', 'hemoglobin', 'height(cm)', 'triglyceride', 'waist(cm)', 'LDL', 'HDL',
                     'Cholesterol', 'ALT', 'fasting blood sugar', 'systolic', 'AST', 'relaxation', 'weight(kg)',
                     'age', 'serum creatinine', 'eyesight(left)', 'eyesight(right)', 'tartar', 'dental caries',
                     'Urine protein', 'hearing(left)', 'hearing(right)']

    # User interface
    gender = st.selectbox("Gender", ["F", "M"])
    val2 = st.slider("Gtp", min_value=1.0, max_value=996.0, step=0.1)
    val3 = st.slider("Hemoglobin", min_value=7.4, max_value=18.7, step=0.1)
    val4 = st.slider("Height (cm)", min_value=100.0, max_value=230.0, step=0.1)
    val5 = st.slider("Triglycerides", min_value=31.0, max_value=1029.0, step=0.1)
    val6 = st.slider("Waist (cm)", min_value=80.0, max_value=102.0, step=0.1)
    val7 = st.slider("LDL", min_value=70.0, max_value=300.0, step=0.1)
    val8 = st.slider("HDL", min_value=20.0, max_value=300.0, step=0.1)
    val9 = st.slider("Cholesterol", min_value=300.0, max_value=700.0, step=0.1)
    val10 = st.slider("ALT", min_value=1.0, max_value=996.0, step=0.1)
    val11 = st.slider("Fasting Blood Sugar", min_value=0.0, max_value=126.0, step=0.1)
    val12 = st.slider("Systolic", min_value=0.0, max_value=140.0, step=0.1)
    val13 = st.slider("AST", min_value=10.0, max_value=1543.0, step=0.1)
    val14 = st.slider("Relaxation", min_value=0.0, max_value=120.0, step=0.1)
    val15 = st.slider("Weight (kg)", min_value=35.0, max_value=300.0, step=0.1)
    val16 = st.slider("Age", min_value=0.0, max_value=100.0, step=0.1)
    val17 = st.slider("Serum Creatinine", min_value=0.27, max_value=6.81, step=0.01)
    val18 = st.slider("Eyesight (left)", min_value=0.0, max_value=2.0, step=0.1)
    val19 = st.slider("Eyesight (right)", min_value=0.0, max_value=2.0, step=0.1)
    val20 = st.slider("Urine Protein", min_value=1.0, max_value=6.0, step=0.1)

    hearing_left = st.selectbox("Hearing (left)", ["Normal", "Difficulty"])
    hearing_right = st.selectbox("Hearing (right)", ["Normal", "Difficulty"])
    tartar = st.selectbox("Tartar", ["No", "Yes"])
    dental_caries = st.selectbox("Dental Caries", ["No", "Yes"])

    if st.button("Predict"):
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
            data_normalized = scaler.transform(df_scaled)
            prediction_result = model.predict(data_normalized)[0]
            result_text = class_dict[str(prediction_result)]
            st.write("Prediction:", result_text)

            # Save to database
            save_prediction(gender, val3, result_text, conn)
            st.success("Prediction saved to database.")
        except Exception as e:
            st.error(f"Error during prediction: {e}")

# --- Limitations and Future Improvements Section ---
def limitations_future_improvement():
    st.title("Limitations and Future Improvements")
    st.write('''Some limitations of the dataset that may affect the prediction of our models include:

1. Lack of information regarding the time period for sample collection.
2. Absence of details about the country or city from which the data originates.

It would be beneficial to include these two pieces of information to facilitate the integration of other demographic data.

To improve the dataset:
1. Include demographic variables (e.g., education, income) and physiological indicators (such as exhaled CO levels) to assess the impact of tobacco.
2. Integrate behavioral data (e.g., smoking habits, quit attempts) for a more comprehensive view.
3. Consider cultural influences on smoking behavior and health outcomes.
4. Account for environmental factors (e.g., air quality, proximity to pollutants) in risk assessment.
5. Incorporate user feedback for iterative model improvement and user interface optimization.
         ''')

# --- Main Function ---
def main():
    st.markdown("""
    <style>
    .css-1d391kg { background-color: #FFA07A !important; }
    .css-1aumxhk { color: #FFD700 !important; }
    </style>
    """, unsafe_allow_html=True)

    st.sidebar.title("Menu")
    selection = st.sidebar.radio("Go to", ["Home", "Relevant Data", "Prediction", "Limitations and Future Improvements"])

    # Download files from S3 if we are on AWS
    download_s3_files()

    # Initialize the database
    conn = init_db()

    if selection == "Home":
        home()
    elif selection == "Relevant Data":
        data()
    elif selection == "Prediction":
        prediction(conn)
    elif selection == "Limitations and Future Improvements":
        limitations_future_improvement()

    # Close the database connection
    if conn:
        conn.close()

if __name__ == "__main__":
    main()