import os
import sys
import numpy as np
import pandas as pd

'''----defining more constants----'''
TARGET_COLUMN:str="Result"
PIPELINE_NAME:str="NETWORKSECURITY"
ARTIFACT_DIR:str="Artifacts"
FILE_NAME:str="network_data\Phishing_Websites_Data.csv"

TRAIN_DATA_FILE:str="train.csv"
TEST_DATA_FILE:str="test.csv"

SCHEMA_FILE_PATH:str=os.path.join("data_schema","schema.yaml")

'''----DATA INGESTION CONSTANTS----'''
DATA_INGESTION_COLLECTION_NAME:str="NETWORKDATA"
DATA_INGESTION_DATABASE_NAME :str="HARDIK"
DATA_INGESTION_DIR_NAME :str="DataIngestion"
DATA_INGESTION_FEATURE_STORE_DIR :str="feature_store"
DATA_INGESTION_INGESTED_DIR :str="ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO :float=0.2

'''----DATA VALIDATION CONSTANTS----'''
DATA_VALIDATION_DIR_NAME:str="data_validation"
DATA_VALIDATION_VALID_DIR:str="validated"
DATA_VALIDATION_INVALID_DIR:str="invalid"
DATA_VALIDATION_DRIFT_REPORT_DIR:str="drift_report"
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME:str="report.yaml"

'''----DATA TRANSFORMATION CONSTANTS----'''
DATA_TRANSFORMATION_DIR:str="data_transformation"
DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR:str="transformed"
DATA_TRANSFORMATION_TRANFORMED_OBJECT_DIR:str="transformed_object"
PREPROCESSOR_OBJECT_FILE_PATH:str="preprocessor_object.pkl"

DATA_TRANSFORMATION_IMPUTER_PARAMS:dict={
"missing_values":np.nan,
"n_neighbors":3,
"weights":"uniform",
}
'''----MODEL TRAINING CONSTANTS----'''
MODEL_TRAINER_DIR:str="trained_model"
MODEL_TRAINER_TRAINED_MODEL_FILE_PATH:str="model.pkl"
MODEL_TRAINER_EXPECTED_ACCURACY:float=0.6
MODEL_TRAINER_OVERFITTING_UNDERFITTING_THRESHOLD:float=0.05
SAVED_MODEL_DIR:str=os.path.join("saved_models")
MODEL_FILE_NAME:str="model.pkl"

