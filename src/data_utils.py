import os
import boto3
from joblib import load
import streamlit as st
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def get_file_paths(base_path):
    return {
        'model': os.path.join(base_path, 'random_forest_model_Default.pkl'),
        'scaler': os.path.join(base_path, 'scaler.pkl'),
        'body_image': os.path.join(base_path, 'body.jpg'),
        'gender_smoke': os.path.join(base_path, 'Gender_smoking.png'),
        'gtp': os.path.join(base_path, 'GTP.png'),
        'hemo': os.path.join(base_path, 'hemoglobine_gender.png'),
        'trigly': os.path.join(base_path, 'Triglyceride.png')
    }

def ensure_files(base_path, is_aws, is_lambda, bucket_name='smoking-body-signals-data-dev'):
    try:
        s3 = boto3.client('s3') if is_aws and not is_lambda else None
        paths = get_file_paths(base_path)
        os.makedirs(base_path, exist_ok=True)
        if is_aws and not is_lambda:
            for key, s3_key in [
                ('model', 'src/random_forest_model_Default.pkl'),
                ('scaler', 'src/scaler.pkl'),
                ('body_image', 'src/body.jpg'),
                ('gender_smoke', 'src/Gender_smoking.png'),
                ('gtp', 'src/GTP.png'),
                ('hemo', 'src/hemoglobine_gender.png'),
                ('trigly', 'src/Triglyceride.png')
            ]:
                local_path = paths[key]
                if not os.path.exists(local_path):
                    logging.debug(f"Attempting to download {s3_key} to {local_path}")
                    s3.download_file(bucket_name, s3_key, local_path)
                    logging.debug(f"Downloaded {s3_key} to {local_path}")
        else:
            for key, local_path in paths.items():
                if not os.path.exists(local_path):
                    logging.error(f"File not found: {local_path}. Place it in {base_path}")
                    st.error(f"File not found: {local_path}. Place it in {base_path}")
                    st.stop()
    except Exception as e:
        logging.error(f"File handling error: {e}")
        st.error(f"File handling error: {e}")
        st.stop()

def load_model_and_scaler(model_path, scaler_path):
    try:
        logging.debug(f"Loading model from {model_path}")
        with open(model_path, 'rb') as f:
            model = load(f)
        logging.debug(f"Loading scaler from {scaler_path}")
        with open(scaler_path, 'rb') as f:
            scaler = load(f)
        logging.debug("Model and scaler loaded successfully")
        return model, scaler
    except FileNotFoundError as e:
        logging.error(f"Error loading model or scaler: {e}")
        st.error(f"Error loading model or scaler: {e}")
        st.stop()
    except Exception as e:
        logging.error(f"Unexpected error loading model or scaler: {e}")
        st.error(f"Unexpected error loading model or scaler: {e}")
        st.stop()