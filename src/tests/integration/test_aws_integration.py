import pytest
import os
from data_utils import ensure_files, get_file_paths
import logging

logging.basicConfig(level=logging.DEBUG)

@pytest.fixture
def setup_test_files():
    # Simula un entorno AWS real
    base_path = "/tmp/test_aws"  # Usa /tmp para no interferir con app
    os.makedirs(base_path, exist_ok=True)
    yield base_path
    # Limpieza después
    for file in get_file_paths(base_path).values():
        if os.path.exists(file):
            os.remove(file)

def test_s3_integration(setup_test_files):
    base_path = setup_test_files
    # Simula is_aws=True, is_lambda=False (EC2 real)
    ensure_files(base_path, is_aws=True, is_lambda=False)
    # Verifica que los archivos clave se descargaron (o no falló)
    paths = get_file_paths(base_path)
    assert os.path.exists(paths['model'])  # random_forest_model_Default.pkl debería estar