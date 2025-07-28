import pytest
from unittest.mock import Mock, patch, mock_open
from data_utils import load_model_and_scaler, ensure_files, get_file_paths

def test_get_file_paths():
    base_path = '/test/path'
    paths = get_file_paths(base_path)
    assert paths['model'] == '/test/path/random_forest_model_Default.pkl'

@patch('data_utils.load')
@patch('builtins.open')
def test_load_model_and_scaler(mock_open, mock_load):
    mock_model = Mock()
    mock_scaler = Mock()
    mock_load.side_effect = [mock_model, mock_scaler]
    model, scaler = load_model_and_scaler('model_path', 'scaler_path')
    assert model == mock_model
    assert scaler == mock_scaler

@patch('data_utils.boto3.client')
@patch('data_utils.os.path.exists', return_value=False)
@patch('data_utils.os.makedirs')
def test_ensure_files_aws(mock_makedirs, mock_exists, mock_s3_client):
    mock_s3 = Mock()
    mock_s3.download_file = Mock()
    mock_s3_client.return_value = mock_s3
    ensure_files('/base', True, False)
    assert mock_s3.download_file.call_count == 7