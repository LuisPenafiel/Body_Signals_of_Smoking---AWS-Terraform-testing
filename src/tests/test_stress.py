import pytest
from prediction import prediction
from unittest.mock import Mock, patch
import time

def test_stress_prediction(mock_model, mock_scaler):
    mock_db = Mock()
    is_aws = False

    start_time = time.time()
    for i in range(10):  # 10 predicciones rápidas
        with patch('streamlit.form_submit_button', return_value=True):
            with patch('streamlit.selectbox', return_value="M"):
                with patch('streamlit.slider', return_value=100.0):
                    prediction(mock_db, mock_model, mock_scaler, is_aws)
    end_time = time.time()
    assert end_time - start_time < 5  # Debe tomar menos de 5 seg
    assert mock_db.save_prediction.call_count == 10  # 10 saves