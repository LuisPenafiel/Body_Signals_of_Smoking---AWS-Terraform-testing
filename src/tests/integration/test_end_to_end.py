import pytest
import os
from app import main as app_main
import streamlit as st
from db_utils import DatabaseManager
from data_utils import get_file_paths, load_model_and_scaler, ensure_files

@pytest.fixture
def setup_end_to_end():
    # Configura entorno simulado
    base_path = "/tmp/end_to_end_test"
    os.makedirs(base_path, exist_ok=True)  # Crea dir
    # Descarga archivos de S3 al dir temporal (simula EC2)
    ensure_files(base_path, is_aws=True, is_lambda=False)  # Añadido para descargar files
    paths = get_file_paths(base_path)
    # Carga modelo y scaler
    model, scaler = load_model_and_scaler(paths['model'], paths['scaler'])
    db = DatabaseManager(is_aws=False, is_lambda=False)  # DB local
    yield {"model": model, "scaler": scaler, "db": db, "base_path": base_path}
    # Limpieza
    db.close()
    for file in paths.values():
        if os.path.exists(file):
            os.remove(file)
    os.rmdir(base_path)

def test_end_to_end_workflow(setup_end_to_end, monkeypatch):
    data = setup_end_to_end
    model, scaler, db, base_path = data["model"], data["scaler"], data["db"], data["base_path"]

    # Monkeypatch para simular UI
    def mock_selectbox(*args, **kwargs):
        return "M"
    def mock_slider(*args, **kwargs):
        return 100.0
    monkeypatch.setattr(st, "selectbox", mock_selectbox)
    monkeypatch.setattr(st, "slider", mock_slider)
    monkeypatch.setattr(st, "form_submit_button", lambda *args: True)

    # Corre app_main
    app_main()

    # Verifica DB
    predictions = db.get_predictions()
    assert len(predictions) > 0
    assert predictions['gender'].iloc[0] == "M"
    assert predictions['prediction'].iloc[0] == "Smoker"  # Basado en mock predict [1]; ajusta si es "Non-Smoker"