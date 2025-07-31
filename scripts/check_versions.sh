#!/bin/bash

echo "1. AWS CLI: $(aws --version | awk '{print $1}' | tr '/' ' ' | awk '{print $2}')"
echo "2. Terraform: $(terraform --version | head -1 | awk '{print $2}')"
echo "3. Python: $(python3 --version | awk '{print $2}')"
echo "4. pip: $(pip3 --version | awk '{print $2}')"
echo "5. Streamlit: $(streamlit --version | awk '{print $3}' | sed 's/,//')"
echo "6. pandas: $(python3 -c "import pandas as pd; print(pd.__version__)")"
echo "7. numpy: $(python3 -c "import numpy as np; print(np.__version__)")"
echo "8. scikit-learn: $(python3 -c "import sklearn; print(sklearn.__version__)")"
echo "9. boto3: $(python3 -c "import boto3; print(boto3.__version__)")"
echo "10. MySQL Connector: $(python3 -c "import mysql.connector; print(mysql.connector.__version__)")"
echo "11. Pillow: $(python3 -c "import PIL; print(PIL.__version__)")"