import os
import boto3
from pickle import load
import streamlit as st
import pandas as pd
from PIL import Image
from sklearn.preprocessing import StandardScaler
import mysql.connector
import sqlite3

# --- Environment Detection ---
IS_AWS = 'AWS_REGION' in os.environ

# --- S3 Configuration (only for AWS) ---
if IS_AWS:
    BUCKET_NAME = 'smoking-body-signals-data-dev'
    REGION_NAME = 'eu-central-1'
    s3 = boto3.client('s3', region_name=REGION_NAME)
    BASE_PATH = '/tmp'  # On AWS, use /tmp for temporary files
else:
    BASE_PATH = '/workspaces/Body_Signals_of_Smoking---AWS-Terraform-testing/src'  # On Codespaces

MODEL_PATH = os.path.join(BASE_PATH, 'random_forest_model_Default.pkl')
SCALER_PATH = os.path.join(BASE_PATH, 'scaler.pkl')
BODY_IMAGE_PATH = os.path.join(BASE_PATH, 'body.jpg')
GENDER_SMOKE_PATH = os.path.join(BASE_PATH, 'Gender_smoking.png')
GTP_PATH = os.path.join(BASE_PATH, 'GTP.png')
HEMO_PATH = os.path.join(BASE_PATH, 'hemoglobine_gender.png')
TRIGLY_PATH = os.path.join(BASE_PATH, 'Triglyceride.png')

# --- Function to Download Files from S3 (only on AWS) ---
def download_s3_files():
    if not IS_AWS:
        return
    try:
        s3.download_file(BUCKET_NAME, 'random_forest_model_Default.pkl', MODEL_PATH)  # No "src/" prefix
        s3.download_file(BUCKET_NAME, 'scaler.pkl', SCALER_PATH)
        s3.download_file(BUCKET_NAME, 'body.jpg', BODY_IMAGE_PATH)
        s3.download_file(BUCKET_NAME, 'Gender_smoking.png', GENDER_SMOKE_PATH)
        s3.download_file(BUCKET_NAME, 'GTP.png', GTP_PATH)
        s3.download_file(BUCKET_NAME, 'hemoglobine_gender.png', HEMO_PATH)
        s3.download_file(BUCKET_NAME, 'Triglyceride.png', TRIGLY_PATH)
    except Exception as e:
        print(f"Error downloading from S3: {e}")

# --- Database Configuration ---
if IS_AWS:
    DB_CONFIG = {
        'host': 'your-rds-endpoint.eu-central-1.rds.amazonaws.com',
        'user': 'admin',
        'password': os.environ.get('DB_PASSWORD', 'defaultpassword'),  # Use env for security
        'database': 'smoking_db'
    }
    def init_db():
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS predictions 
                (id INT AUTO_INCREMENT PRIMARY KEY, gender VARCHAR(10), hemoglobin FLOAT, prediction VARCHAR(20), timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
            """)
            conn.commit()
            return conn
        except mysql.connector.Error as e:
            st.error(f"Error connecting to MySQL: {e}")
            st.stop()
else:
    DB_PATH = '/workspaces/Body_Signals_of_Smoking---AWS-Terraform-testing/data/predictions.db'
    def init_db():
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS predictions 
                (id INTEGER PRIMARY KEY AUTOINCREMENT, gender TEXT, hemoglobin REAL, prediction TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)
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
            cursor.execute("INSERT INTO predictions (gender, hemoglobin, prediction) VALUES (%s, %s, %s)", (gender, hemoglobin, prediction))
        else:
            cursor.execute("INSERT INTO predictions (gender, hemoglobin, prediction) VALUES (?, ?, ?)", (gender, hemoglobin, prediction))
        conn.commit()
    except (mysql.connector.Error, sqlite3.Error) as e:
        st.error(f"Error saving to database: {e}")

# --- Sections (from current, with fixes) ---
def home():
    st.markdown("<div class='header'><h1><i class='fas fa-lungs'></i> Body Signals of Smoking</h1><p class='slogan animate__animated animate__fadeIn'>Empowering Health Awareness</p></div>", unsafe_allow_html=True)
    # ... (rest of home code)

def data():
    st.header("Relevant Data Insights")
    # ... (rest of data code)

def limitations_future_improvement():
    st.header("Research Insights")
    # ... (rest of limitations code)

def prediction(conn):
    st.header("Smoking Prediction :no_smoking:")
    # ... (rest of prediction code, including model load with try/except)

# --- Main Function ---
def main():
    st.set_page_config(page_title="Body Signals of Smoking", layout="wide", initial_sidebar_state="expanded")
    # ... (styles)

    st.sidebar.title("Menu")
    selection = st.sidebar.radio("Navigation", ["Home", "Relevant Data", "Prediction", "Limitations"], label_visibility="collapsed")

    download_s3_files()
    conn = init_db()

    if selection == "Home":
        home()
    elif selection == "Relevant Data":
        data()
    elif selection == "Prediction":
        prediction(conn)
    elif selection == "Limitations":
        limitations_future_improvement()

    if conn:
        conn.close()

if __name__ == "__main__":
    main()