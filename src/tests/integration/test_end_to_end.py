import pytest
import os
import streamlit as st
from db_utils import DatabaseManager
from data_utils import get_file_paths, load_model_and_scaler, ensure_files

from prediction import prediction

@pytest.fixture
def setup_end_to_end():
    # Configura entorno simulado
    base_path = "/tmp/end_to_end_test"
    os.makedirs(base_path, exist_ok=True)
    # Descarga archivos de S3 al dir temporal
    ensure_files(base_path, is_aws=True, is_lambda=False)
    paths = get_file_paths(base_path)
    # Carga modelo y scaler
    model, scaler = load_model_and_scaler(paths['model'], paths['scaler'])
    # Delete old DB if exists to clean
    db_path = 'predictions.db'
    if os.path.exists(db_path):
        os.remove(db_path)
        print("Old DB deleted for clean test")
    db = DatabaseManager(is_aws=False, is_lambda=False)  # New clean DB
    yield {"model": model, "scaler": scaler, "db": db, "base_path": base_path}
    # Limpieza
    db.close()
    if os.path.exists(db_path):
        os.remove(db_path)
    for file in paths.values():
        if os.path.exists(file):
            os.remove(file)
    if os.path.exists(base_path):
        os.rmdir(base_path)

def test_end_to_end_workflow(setup_end_to_end, monkeypatch):
    data = setup_end_to_end
    model, scaler, db, base_path = data["model"], data["scaler"], data["db"], data["base_path"]

    # Monkeypatch para simular UI
    def mock_selectbox(label, options):
        print(f"Selectbox called with label: '{label}', options: {options}")  # Debug
        if "Gender" in label:
            print("Matching Gender - returning 'M'")
            return "M"
        if "Hearing (Left)" in label:
            print("Hearing Left - returning 'Normal'")
            return "Normal"
        if "Hearing (Right)" in label:
            print("Hearing Right - returning 'Normal'")
            return "Normal"
        if "Tartar" in label:
            print("Tartar - returning 'No'")
            return "No"
        if "Dental Caries" in label:
            print("Dental Caries - returning 'No'")
            return "No"
        print(f"No match - returning {options[0]}")
        return options[0] if options else None

    def mock_slider(label, *args, **kwargs):
        print(f"Slider called with label: '{label}'")  # Debug
        # Retorna valores basados en label
        if "Hemoglobin" in label:
            return 15.0  # Alto for Smoker
        return 100.0

    monkeypatch.setattr(st, "selectbox", mock_selectbox)
    monkeypatch.setattr(st, "slider", mock_slider)
    monkeypatch.setattr(st, "form_submit_button", lambda *args: True)

    # Llama prediction
    prediction(db, model, scaler, is_aws=False)

    # Verifica DB
    predictions = db.get_predictions()
    print(f"Predictions DF: {predictions}")  # Debug to see the DF
    assert len(predictions) > 0
    assert predictions['gender'].iloc[0] == "M"
    assert predictions['prediction'].iloc[0] in ["Smoker", "Non-Smoker"]