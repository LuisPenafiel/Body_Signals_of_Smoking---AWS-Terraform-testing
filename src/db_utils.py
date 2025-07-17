import os
import json
import boto3
import sqlite3
import logging  # NEW: Logging

logging.basicConfig(filename=os.path.join(os.path.dirname(__file__), 'db.log'), level=logging.DEBUG)

class DatabaseManager:
    def __init__(self, is_aws, is_lambda):
        self.is_aws = is_aws
        self.is_lambda = is_lambda
        if self.is_aws:
            self.s3 = boto3.client('s3')
            self.bucket = 'smoking-body-signals-data-dev'
            logging.debug("DB Manager initialized for AWS/S3")
        else:
            db_path = os.path.join(os.path.dirname(__file__), 'predictions.db')
            self.conn = sqlite3.connect(db_path)
            self.cursor = self.conn.cursor()
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS predictions 
                                (gender TEXT, hemoglobin REAL, result TEXT)''')
            self.conn.commit()
            logging.debug("DB Manager initialized for local SQLite")

    def save_prediction(self, gender, hemoglobin, result, is_aws):  # is_aws pasado por compatibilidad
        if self.is_aws:
            data = {'gender': gender, 'hemoglobin': hemoglobin, 'result': result}
            key = f'predictions/{gender}_{hemoglobin}_{os.urandom(4).hex()}.json'  # Unique key
            self.s3.put_object(Bucket=self.bucket, Key=key, Body=json.dumps(data))
            logging.info(f"Saved prediction to S3: {key}")
        else:
            self.cursor.execute('INSERT INTO predictions (gender, hemoglobin, result) VALUES (?, ?, ?)',
                                (gender, hemoglobin, result))
            self.conn.commit()
            logging.info("Saved prediction to local DB")

    def close(self):
        if not self.is_aws:
            self.conn.close()
            logging.debug("Local DB closed")