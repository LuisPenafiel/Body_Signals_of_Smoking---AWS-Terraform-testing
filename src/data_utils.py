import os
import boto3
from joblib import load
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
            for key, s3_key in [('model', 'src/random_forest_model_Default.pkl'),
                                ('scaler', 'src/scaler.pkl'),
                                ('body_image', 'src/body.jpg'),
                                ('gender_smoke', 'src/Gender_smoking.png'),
                                ('gtp', 'src/GTP.png'),
                                ('hemo', 'src/hemoglobine_gender.png'),
                                ('trigly', 'src/Triglyceride.png')]:
                local_path = paths[key]
                if not os.path.exists(local_path):
                    logging.warning(f"File {local_path} not found, attempting download from {s3_key}")
                    s3.download_file(bucket_name, s3_key, local_path)
                    logging.info(f"Downloaded {s3_key} from S3.")
        else:
            for key, local_path in paths.items():
                if not os.path.exists(local_path):
                    logging.error(f"File not found: {local_path}.")
    except Exception as e:
        logging.error(f"File handling error: {e}")
        raise

def load_model_and_scaler(model_path, scaler_path):
    try:
        logging.info(f"Loading model from {model_path} and scaler from {scaler_path}")
        model = load(model_path)
        scaler = load(scaler_path)
        logging.info("Model and scaler loaded successfully")
        return model, scaler
    except Exception as e:
        logging.error(f"Error loading model or scaler: {e}")
        raise