import pytest
from unittest.mock import Mock, patch
from botocore.exceptions import ClientError  # Añade esto para simular error real de AWS
from db_utils import DatabaseManager

@patch('db_utils.sqlite3.connect')
@patch('db_utils.boto3.client')
def test_database_manager_init_aws(mock_s3_client, mock_connect):
    mock_s3 = Mock()
    # Simula el error real de AWS (ClientError 404, como en db_utils.py)
    mock_s3.download_file.side_effect = ClientError({'Error': {'Code': '404'}}, 'download_file')
    mock_s3_client.return_value = mock_s3
    db = DatabaseManager(True, False)  # El código maneja el error y crea DB
    mock_connect.assert_called()  # Verifica que se llama create_db después del error

@patch('db_utils.sqlite3.connect')
def test_save_prediction(mock_connect):
    db = DatabaseManager(False, False)
    mock_cursor = Mock()
    mock_conn = Mock()
    mock_conn.cursor.return_value = mock_cursor
    mock_connect.return_value = mock_conn
    db.save_prediction('M', 15.0, 'Smoker', False)
    mock_cursor.execute.assert_called()  # Verifica insert