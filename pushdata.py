import os
import sys
import json

from dotenv import load_dotenv

load_dotenv()
MONGO_DB_URL=os.getenv("MONGO_DB_URL")
print(MONGO_DB_URL)

import certifi
#Create root certificates and HTTPS connection so that the DB knows that this is a valid request
ca=certifi.where() #ca is certificateAuthorities , verify SSL ,TSL connections

import pandas as pd
import numpy as np
import pymongo
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

class NetworkDataExtraction():
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    def csv_to_json_converter(self,filepath):
        try:
            df=pd.read_csv(filepath)
            df.reset_index(drop=True,inplace=True)
            records= list(json.loads((df.T.to_json())).values())
            return records
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    def insert_data_mongodb(self,records,database,collection):
        try:
            self.collection=collection
            self.database=database
            self.records=records
            self.mongo_client=pymongo.MongoClient(MONGO_DB_URL)
            self.database=self.mongo_client[self.database]
            self.collection=self.database[self.collection]
            self.collection.insert_many(self.records)
            return (len(self.records))
        except Exception as e:
            raise NetworkSecurityException(e,sys)
            
if __name__=="__main__":
    FILE_PATH="network_data\Phishing_Legitimate_full.csv"
    DATABASE="HARDIK"
    COLLECTION="NETWORKDATA"
    
    network=NetworkDataExtraction()
    records=network.csv_to_json_converter(FILE_PATH)    
    recordno=network.insert_data_mongodb(records,DATABASE,COLLECTION)
    print(records)
    print(recordno)