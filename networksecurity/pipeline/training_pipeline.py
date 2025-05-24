import os,sys
from datetime import datetime

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

from networksecurity.components.DataIngestion import DataIngestion
from networksecurity.components.DataValidation import DataValidation
from networksecurity.components.DataTranformation import DataTransformation
from networksecurity.components.Model_trainer import ModelTrainer

from networksecurity.entity.config_entity import DataIngestionConfig,DataTransformationConfig,DataValidationConfig,ModelTrainerConfig,TrainingPipelineConfig

from networksecurity.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact,DataTransformationArtifact,ModelTrainerArtifact
from networksecurity.constant.training_pipeline import TRAINING_BUCKET_NAME
from networksecurity.cloud.s3_syncer import S3_syncer

class TrainingPipeline:
    def __init__(self):
        self.training_pipeline_config = TrainingPipelineConfig(timestamp=datetime.now())
        self.s3_sync=S3_syncer()
    def start_ingestion(self)->DataIngestionArtifact:
        try:
            self.data_ingestion_config=DataIngestionConfig(self.training_pipeline_config)
            self.dataingestion=DataIngestion(self.data_ingestion_config)
            logging.info("Start the data ingestion")
            data_ingestion_artifact=self.dataingestion.initiate_data_ingestion()
            logging.info(f"{data_ingestion_artifact} is created as a result of data ingestion")

            return data_ingestion_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    def start_validation(self,data_ingestion_artifact:DataIngestionArtifact)->DataValidationArtifact:
        try:

            self.data_validation_config=DataValidationConfig(self.training_pipeline_config)
            self.data_validation=DataValidation(data_ingestion_artifact,self.data_validation_config)
            logging.info("Start the data validation")
            data_validation_artifact=self.data_validation.initiate_data_validation()
            logging.info(f"{data_validation_artifact} is created as a result of data validation")
            return data_validation_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def start_tranformation(self,data_validation_artifact:DataValidationArtifact)->DataTransformationArtifact:
        try:
            self.data_transformation_config=DataTransformationConfig(self.training_pipeline_config)
            self.data_transformation=DataTransformation(data_validation_artifact,self.data_transformation_config)
            logging.info("Start the data transformation")
            data_transformation_artifact=self.data_transformation.initiate_data_transformation()
            logging.info(f"{data_transformation_artifact} is created as a result of data transformation")
            return data_transformation_artifact
 
        except Exception as e:
            raise NetworkSecurityException(e,sys)
   
    def start_model_training(self,data_transformation_artifact:DataTransformationArtifact)->ModelTrainerArtifact:
        try:
            self.model_training_config=ModelTrainerConfig(self.training_pipeline_config)
            self.model_trainer=ModelTrainer(data_transformation_artifact=data_transformation_artifact, model_trainer_config=self.model_training_config)
            logging.info("Start the model training")
            model_trainer_artifact=self.model_trainer.initiate_model_trainer()
            logging.info(f"{model_trainer_artifact} is created as a result of model training")
            return model_trainer_artifact
        
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    def sync_artificat_dir_s3(self):
        try:
            aws_url=f"s3://{TRAINING_BUCKET_NAME}/artifact/{self.training_pipeline_config.timestamp}"
            self.S3_syncer.sync_folder_to_s3(folder=self.training_pipeline_config.artifact_dir,aws_bucket_url=aws_url)
            
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def sync_model_dir_s3(self):
        try:
            aws_url=f"s3://{TRAINING_BUCKET_NAME}/final_models/{self.training_pipeline_config.timestamp}"
            self.s3_sync.sync_folder_to_s3(folder=self.training_pipeline_config.model_dir,aws_bucket_url=aws_url)
            
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    def start_pipeline(self):
        try:
            data_ingestion_artifact:DataIngestionArtifact=self.start_ingestion()
            data_validation_artifact:DataValidationArtifact=self.start_validation(data_ingestion_artifact)
            data_transformation_artifact:DataTransformationArtifact=self.start_tranformation(data_validation_artifact)
            model_trainer_artifact:ModelTrainerArtifact=self.start_model_training(data_transformation_artifact)

            self.sync_artificat_dir_s3()
            self.sync_model_dir_s3()
            return model_trainer_artifact
        except Exception as e:
            return NetworkSecurityException(e,sys)

                   