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
    """Asegura que los archivos necesarios estén disponibles, descargándolos de S3 si es necesario."""
    try:
        s3 = boto3.client('s3', region_name=region_name) if is_aws and not is_lambda else None
        paths = get_file_paths(base_path)
        if is_aws and not is_lambda:
            for key, s3_key in [('model', 'src/random_forest_model_Default.pkl'),
                                ('scaler', 'src/scaler.pkl'),
                                ('body_image', 'src/body.jpg'),
                                ('gender_smoke', 'src/Gender_smoking.png'),
                                ('gtp', 'src/GTP.png'),
                                ('hemo', 'src/hemoglobine_gender.png'),
                                ('trigly', 'src/Triglyceride.png')]:
                local_path = paths[key]
                if not os.path.exists(local_path):
                    s3.download_file(bucket_name, s3_key, local_path)
                    logging.info(f"Downloaded {s3_key} from S3.")  # NEW: Log en vez de st.success
        else:
            for key, local_path in paths.items():
                if not os.path.exists(local_path):
                    logging.error(f"File not found: {local_path}. Place it in {base_path}.")  # FIXED: Log, no st.error/stop
                    # No st.stop() - permite app continue
    except Exception as e:
        logging.error(f"File handling error: {e}")  # FIXED: Log, no st.rerun()

def load_model_and_scaler(model_path, scaler_path):
    """Carga el modelo y el escalador desde los archivos especificados."""
    with open(model_path, 'rb') as f:
        model = load(f)
    with open(scaler_path, 'rb') as f:
        scaler = load(f)
    return model, scaler  # Exception handled in caller