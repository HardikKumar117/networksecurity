from networksecurity.constant.training_pipeline import SAVED_MODEL_DIR,MODEL_FILE_NAME
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
import os,sys

class NetworkModel:
    def __init__(self,processor,model):
        try:
           self.processor=processor
           self.model=model
        except Exception as e:
           raise NetworkSecurityException(e,sys)
        
    def predict(self,x):
        try:
            x_transform=self.processor(x)
            prediction=self.model.predict(x_transform)
            return prediction
        except Exception as e:
            raise NetworkSecurityException(e,sys)