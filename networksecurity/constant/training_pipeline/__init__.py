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

'''----DATA INGESTION CONSTANTS----'''
DATA_INGESTION_COLLECTION_NAME:str="NETWORKDATA"
DATA_INGESTION_DATABASE_NAME :str="HARDIK"
DATA_INGESTION_DIR_NAME :str="DataIngestion"
DATA_INGESTION_FEATURE_STORE_DIR :str="feature_store"
DATA_INGESTION_INGESTED_DIR :str="ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO :float=0.2