import pytest
from unittest.mock import Mock
from typing import Any

@pytest.fixture
def mock_model():
    model = Mock()
    model.predict.return_value = [1]  # Simula una predicción de "Smoker"
    model.feature_names_in_ = ['gender', 'Gtp', 'hemoglobin', 'height(cm)', 'triglyceride', 'waist(cm)', 'LDL', 'HDL',
                               'Cholesterol', 'ALT', 'fasting blood sugar', 'systolic', 'AST', 'relaxation', 'weight(kg)',
                               'age', 'serum creatinine', 'eyesight(left)', 'eyesight(right)', 'tartar', 'dental caries',
                               'Urine protein', 'hearing(left)', 'hearing(right)']  # Todas las variables de tu modelo
    return model

@pytest.fixture
def mock_scaler():
    scaler = Mock()
    scaler.transform.return_value = [[0.5] * 24]  # Datos falsos escalados (24 variables)
    return scaler

@pytest.fixture
def mock_s3_client():
    s3_client = Mock()
    s3_client.download_file = Mock()
    return s3_client