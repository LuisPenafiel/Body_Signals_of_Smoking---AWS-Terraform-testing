import os
import sqlite3
import boto3
import pandas as pd
from botocore.exceptions import ClientError
import logging

class DatabaseManager:
    def __init__(self, is_aws, is_lambda):
        self.is_aws = is_aws
        self.is_lambda = is_lambda
        self.local_db_path = '/tmp/predictions.db' if is_aws else 'predictions.db'
        
        if is_aws:
            self.s3_bucket = 'smoking-body-signals-data-dev'
            self.s3_key = 'predictions.db'
            self.setup_aws_db()
        else:
            self.setup_local_db()
    
    def setup_aws_db(self):
        s3 = boto3.client('s3')
        try:
            s3.download_file(self.s3_bucket, self.s3_key, self.local_db_path)
        except ClientError as e:
            if e.response['Error']['Code'] == '404':
                self.create_db()
                self.upload_to_s3()
            else:
                raise
    
    def setup_local_db(self):
        if not os.path.exists(self.local_db_path):
            self.create_db()
    
    def create_db(self):
        conn = sqlite3.connect(self.local_db_path)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS predictions (
                     id INTEGER PRIMARY KEY AUTOINCREMENT,
                     gender TEXT,
                     hemoglobin REAL,
                     prediction TEXT,
                     timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
        conn.commit()
        conn.close()
    
    # FIX: Add is_aws parameter to match the call
    def save_prediction(self, gender, hemoglobin, prediction, is_aws):
        conn = sqlite3.connect(self.local_db_path)
        c = conn.cursor()
        c.execute("INSERT INTO predictions (gender, hemoglobin, prediction) VALUES (?, ?, ?)", 
                  (gender, hemoglobin, prediction))
        conn.commit()
        conn.close()
        
        # Upload to S3 if we're in AWS environment
        if is_aws:
            self.upload_to_s3()
    
    def upload_to_s3(self):
        s3 = boto3.client('s3')
        s3.upload_file(self.local_db_path, self.s3_bucket, self.s3_key)
    
    def get_predictions(self):
        conn = sqlite3.connect(self.local_db_path)
        df = pd.read_sql_query("SELECT * FROM predictions", conn)
        conn.close()
        return df
    
    def close(self):
        if self.is_aws:
            self.upload_to_s3()