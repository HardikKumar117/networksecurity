from networksecurity.components.DataIngestion import DataIngestion
from networksecurity.components.DataValidation import DataValidation
from networksecurity.components.DataTranformation import DataTransformation
from networksecurity.entity.config_entity import DataIngestionConfig,TrainingPipelineConfig,DataValidationConfig,DataTransformationConfig
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
        data_validation_config=DataValidationConfig(training_pipeline_config)
        data_validation = DataValidation(dataingestionartifact, data_validation_config)
        logging.info("initiate the data validation")
        data_validation_artifact = data_validation.initiate_data_validation()
        logging.info("data validation is completed")
        print(data_validation_artifact)
        data_transformation_config=DataTransformationConfig(training_pipeline_config)
        data_transformation=DataTransformation(data_validation_artifact,data_transformation_config)
        data_transformation_artifact=data_transformation.initiate_data_transformation()
        print(data_transformation_artifact)
        logging.info("data transformation is completed")
        

       
    except Exception as e:
        raise NetworkSecurityException(e,sys)
