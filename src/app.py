import os
import streamlit as st
from PIL import Image
from data_utils import get_file_paths, ensure_files, load_model_and_scaler
from db_utils import DatabaseManager
from prediction import prediction

# --- Environment Detection ---
IS_AWS = 'AWS_REGION' in os.environ or 'AWS_LAMBDA_FUNCTION_NAME' in os.environ
IS_LAMBDA = 'AWS_LAMBDA_FUNCTION_NAME' in os.environ

# --- S3 and File Configuration ---
BUCKET_NAME = 'smoking-body-signals-data-dev'
REGION_NAME = 'eu-central-1'
BASE_PATH = '/tmp' if IS_AWS else '/workspaces/Body_Signals_of_Smoking---AWS-Terraform-testing/src'
paths = get_file_paths(BASE_PATH)

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

    ensure_files(BASE_PATH, IS_AWS, IS_LAMBDA)
    db = DatabaseManager(IS_AWS, IS_LAMBDA)  # Pass environment flags
    model, scaler = load_model_and_scaler(paths['model'], paths['scaler'])

    if selection == "Home":
        home()
    elif selection == "Relevant Data":
        data()
    elif selection == "Prediction":
        # FIX: Pass IS_AWS as additional argument
        prediction(db, model, scaler, IS_AWS)  # <-- IMPORTANT CHANGE HERE
    elif selection == "Limitations":
        limitations_future_improvement()

    db.close()

if __name__ == "__main__":
    main()