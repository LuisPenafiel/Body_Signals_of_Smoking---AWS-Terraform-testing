import pytest
import os
from app import main as app_main  # Importa la función principal
import streamlit as st
from db_utils import DatabaseManager
from data_utils import get_file_paths, load_model_and_scaler

@pytest.fixture
def setup_end_to_end():
    # Configura entorno simulado
    base_path = "/tmp/end_to_end_test"
    os.makedirs(base_path, exist_ok=True)
    paths = get_file_paths(base_path)
    # Simula carga de modelo y scaler (usa paths reales de EC2)
    model, scaler = load_model_and_scaler(paths['model'], paths['scaler'])
    db = DatabaseManager(is_aws=False, is_lambda=False)  # Local para test
    yield {"model": model, "scaler": scaler, "db": db, "base_path": base_path}
    # Limpieza
    db.close()
    for file in paths.values():
        if os.path.exists(file):
            os.remove(file)

def test_end_to_end_workflow(setup_end_to_end, monkeypatch):
    # Simula entrada del usuario
    data = setup_end_to_end
    model, scaler, db, base_path = data["model"], data["scaler"], data["db"], data["base_path"]

    # Monkeypatch para simular UI inputs
    def mock_selectbox(*args, **kwargs):
        return "M"  # Simula género masculino
    def mock_slider(*args, **kwargs):
        return 100.0  # Valor fijo para sliders
    monkeypatch.setattr(st, "selectbox", mock_selectbox)
    monkeypatch.setattr(st, "slider", mock_slider)
    monkeypatch.setattr(st, "form_submit_button", lambda *args: True)  # Simula botón click

    # Llama la función principal (simula app)
    app_main()  # Esto ejecuta prediction y guarda en DB

    # Verifica que se guardó en DB
    predictions = db.get_predictions()
    assert len(predictions) > 0  # Debería tener al menos 1 predicción
    assert predictions['gender'].iloc[0] == "M"  # Verifica género
    assert predictions['prediction'].iloc[0] in ["Smoker", "Non-Smoker"]  # Verifica predicción