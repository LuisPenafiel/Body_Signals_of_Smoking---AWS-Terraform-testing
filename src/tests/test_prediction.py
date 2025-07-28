import pytest
from unittest.mock import Mock, patch
from prediction import prediction

@patch('prediction.st.form_submit_button', return_value=True)  # Simula botón "Predict"
@patch('prediction.st.success')  # Mock UI success
def test_prediction_function(mock_success, mock_submit, mock_model, mock_scaler):
    mock_db = Mock()
    is_aws = False

    # Mock sliders/selects with fixed values
    with patch('prediction.st.slider', side_effect=[100.0, 12.0, 170.0, 150.0, 90.0, 100.0, 50.0, 200.0, 20.0, 90.0, 120.0, 25.0, 80.0, 70.0, 30.0, 1.0, 1.0, 1.0, 1.0]):
        with patch('prediction.st.selectbox', side_effect=['M', 'Normal', 'Normal', 'Yes', 'Yes']):  # Mock selects
            prediction(mock_db, mock_model, mock_scaler, is_aws)

    mock_success.assert_called_with("Prediction: **Smoker**")  # Verifica que se llama UI con 'Smoker'