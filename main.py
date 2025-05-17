from networksecurity.components.DataIngestion import DataIngestion
from networksecurity.entity.config_entity import DataIngestionConfig,TrainingPipelineConfig
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging  
from datetime import datetime
import sys

if __name__ == "__main__":
    try:
        training_pipeline_config=TrainingPipelineConfig(timestamp=datetime.now())
        data_ingestion_config=DataIngestionConfig(training_pipeline_config)
        dataingestion=DataIngestion(data_ingestion_config)
        logging.info("initiate data ingestion")
        dataingestionartifact=dataingestion.initiate_data_ingestion()
        print(dataingestionartifact)
    except Exception as e:
        raise NetworkSecurityException(e,sys)
