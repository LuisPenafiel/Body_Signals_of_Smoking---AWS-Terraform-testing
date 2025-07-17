import os
import boto3
from pickle import load
import streamlit as st
import logging  # NEW: Log errors

logging.basicConfig(filename=os.path.join(os.path.dirname(__file__), 'data.log'), level=logging.DEBUG)

def get_file_paths(base_path):
    """Devuelve un diccionario con las rutas de los archivos necesarios."""
    return {
        'model': os.path.join(base_path, 'random_forest_model_Default.pkl'),
        'scaler': os.path.join(base_path, 'scaler.pkl'),
        'body_image': os.path.join(base_path, 'body.jpg'),
        'gender_smoke': os.path.join(base_path, 'Gender_smoking.png'),
        'gtp': os.path.join(base_path, 'GTP.png'),
        'hemo': os.path.join(base_path, 'hemoglobine_gender.png'),
        'trigly': os.path.join(base_path, 'Triglyceride.png')
    }

def ensure_files(base_path, is_aws, is_lambda, bucket_name='smoking-body-signals-data-dev', region_name='eu-central-1'):
    logging.debug(f"Ensuring files in {base_path}, is_aws={is_aws}")
    print(f"Ensuring files in {base_path}")  # NEW: Print for manual debug
    try:
        s3 = boto3.client('s3', region_name=region_name) if is_aws and not is_lambda else None
        paths = get_file_paths(base_path)
        if is_aws and not is_lambda:
            for key, s3_key in [ ... ]:  # Lista sin cambios
                local_path = paths[key]
                if not os.path.exists(local_path):
                    logging.info(f"Downloading {s3_key}")
                    print(f"Downloading {s3_key}")  # NEW
                    s3.download_file(bucket_name, s3_key, local_path)
        else:
            for key, local_path in paths.items():
                if not os.path.exists(local_path):
                    logging.error(f"Missing: {local_path}")
                    print(f"Missing: {local_path}")  # NEW: Print instead of st.error/stop
    except Exception as e:
        logging.error(f"Ensure error: {e}")
        print(f"Ensure error: {e}")  # NEW

def load_model_and_scaler(model_path, scaler_path):
    logging.debug(f"Loading model from {model_path}")
    print(f"Loading model from {model_path}")  # NEW
    try:
        with open(model_path, 'rb') as f:
            model = load(f)
        with open(scaler_path, 'rb') as f:
            scaler = load(f)
        return model, scaler
    except Exception as e:  # Cambiado a general Exception
        logging.error(f"Load error: {e}")
        print(f"Load error: {e}")
        raise  # Re-raise para caller handle