import pymongo
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
import pandas as pd
import numpy as np
from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.artifact_entity import DataIngestionArtifact
import os,sys
import pymongo
from typing import List
from sklearn.model_selection import train_test_split

from dotenv import load_dotenv
from os import getenv
load_dotenv()
MONGO_DB_URL=getenv("MONGO_DB_URL")
class DataIngestion:
    def __init__(self,data_ingestion_config):
        try:
            self.data_ingestion_config=data_ingestion_config
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    def export_as_dataframe(self):
        #reads data from MongoDB
        database=self.data_ingestion_config.database_name
        collection_name=self.data_ingestion_config.collection_name
        self.mongo_client=pymongo.MongoClient(MONGO_DB_URL)
        collection=self.mongo_client[database][collection_name]
        df=pd.DataFrame(list(collection.find()))
        if "_id" in df.columns:
            df.drop(columns=["_id"],inplace=True,axis=1)
            df.replace("na", np.nan, inplace=True)
            return df
    
    def export_data_to_feature_store(self,dataframe:pd.DataFrame):
        try:
            feature_store_file_path=self.data_ingestion_config.feature_store_file_path
            dir_name=os.path.dirname(feature_store_file_path)
            os.makedirs(dir_name,exist_ok=True)
            dataframe.to_csv(feature_store_file_path,index=False,header=True)
            return dataframe
        
        except Exception as e:
            raise NetworkSecurityException
    def split_data_train_test(self,dataframe:pd.DataFrame):
        try:
            train_set,test_set=train_test_split(dataframe,test_size=self.data_ingestion_config.train_test_split_ratio)
            logging.info("Performed train test split")
            logging.info("Exited the split_data_train_test method of DataIngestion class")
            dir_name=os.path.dirname(self.data_ingestion_config.training_path_file_path)
            os.makedirs(dir_name,exist_ok=True)
            logging.info("Exporting train and test file path")
            train_set.to_csv(self.data_ingestion_config.training_path_file_path,index=False,header=True)
            test_set.to_csv(self.data_ingestion_config.testing_path_file_path,index=False,header=True)
            logging.info("Exported data to training and testing path ")
        except Exception as e:
            raise NetworkSecurityException
        
    def initiate_data_ingestion(self):
        try:
            dataframe=self.export_as_dataframe()
            self.export_data_to_feature_store(dataframe)
            self.split_data_train_test(dataframe)
            dataingestionartifact=DataIngestionArtifact(trained_file_path=self.data_ingestion_config.training_path_file_path,test_file_path=self.data_ingestion_config.testing_path_file_path)
            return dataingestionartifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)
   
      



       



