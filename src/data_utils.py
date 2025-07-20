import os
import boto3
from joblib import load  # Usamos joblib para mejor compatibilidad con scikit-learn
import streamlit as st
import logging

logging.basicConfig(level=logging.DEBUG)

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

def ensure_files(base_path, is_aws, is_lambda, bucket_name='smoking-body-signals-data-dev', region_name='eu-central-1'):
    try:
        s3 = boto3.client('s3', region_name=region_name) if is_aws and not is_lambda else None
        paths = get_file_paths(base_path)
        if is_aws and not is_lambda:
            for key, s3_key in [('model', 'random_forest_model_Default.pkl'),
                                ('scaler', 'scaler.pkl'),
                                ('body_image', 'body.jpg'),
                                ('gender_smoke', 'Gender_smoking.png'),
                                ('gtp', 'GTP.png'),
                                ('hemo', 'hemoglobine_gender.png'),
                                ('trigly', 'Triglyceride.png')]:
                local_path = paths[key]
                if not os.path.exists(local_path):
                    s3.download_file(bucket_name, s3_key, local_path)
                    logging.info(f"Downloaded {s3_key} from S3.")
        else:
            for key, local_path in paths.items():
                if not os.path.exists(local_path):
                    logging.error(f"File not found: {local_path}.")
                    # No st.stop(), permitimos continuar con error
    except Exception as e:
        logging.error(f"File handling error: {e}")

def load_model_and_scaler(model_path, scaler_path):
    try:
        model = load(model_path)
        scaler = load(scaler_path)
        return model, scaler
    except Exception as e:
        logging.error(f"Error loading model or scaler: {e}")
        raise