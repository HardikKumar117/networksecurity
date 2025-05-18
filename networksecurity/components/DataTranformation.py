import os,sys
import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline

from networksecurity.constant.training_pipeline import TARGET_COLUMN,DATA_TRANSFORMATION_IMPUTER_PARAMS 
from networksecurity.entity.artifact_entity import DataTransformationArtifact,DataValidationArtifact
from networksecurity.entity.config_entity import DataTransformationConfig 
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.util.main_utils.utils import save_numpy_array_data,save_object
 

class DataTransformation:
    def __init__(self,data_validation_artifact:DataValidationArtifact,data_transformation_config:DataTransformationConfig):
        try:
            self.data_validation_artifact:DataValidationArtifact=data_validation_artifact
            self.data_transformation_config:DataTransformationConfig=data_transformation_config

        except Exception as e:
            raise NetworkSecurityException(e,sys)
    @staticmethod
    def read_data(filepath)->pd.DataFrame:
        try:
            return pd.read_csv(filepath)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    
    def get_transformer_data_object(self)->Pipeline:
        '''Uses KNN imputer to fill the NaN values in the dataset and returns the pipeline object of KNN with the previously defined params'''
        logging.info("Entered the Get_transformer method of the DataTransformation class")
        try:
            imputer=KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS) # double star so that argument is considerd as key value pairs
            processor:Pipeline=Pipeline([("imputer",imputer)])
            logging.info("Exited the transformation method of the DataTransformation class")
            return processor
        
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def initiate_data_transformation(self)->DataTransformationArtifact:
        logging.info("Entering data transformation method")
        try:
            logging.info("Started the transformation")
            train_df=DataTransformation.read_data(self.data_validation_artifact.valid_train_file_path)
            test_df=DataTransformation.read_data(self.data_validation_artifact.valid_test_file_path)

            train_input_features=train_df.drop(columns=[TARGET_COLUMN],axis=1)
            train_target_feature=train_df[TARGET_COLUMN].replace(-1,0)

            test_input_features=test_df.drop(columns=[TARGET_COLUMN],axis=1)
            test_target_feature=test_df[TARGET_COLUMN].replace(-1,0)

            preprocessor_object= self.get_transformer_data_object()
            train_transformed_feature=preprocessor_object.fit_transform(train_input_features)
            test_transformed_feature=preprocessor_object.transform(test_input_features)

            

            train_arr=np.c_[train_transformed_feature,np.array(train_target_feature)]
            test_arr=np.c_[test_transformed_feature,np.array(test_target_feature)]
            
            save_numpy_array_data(self.data_transformation_config.transformed_train_file_path,train_arr)
            save_numpy_array_data(self.data_transformation_config.transformed_test_file_path,test_arr)
            save_object(self.data_transformation_config.data_transformation_object_file_path,preprocessor_object)

            logging.info("Savedd the data and object files")

            data_transformation_artifact=DataTransformationArtifact(
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path,
                transformed_object_file_path=self.data_transformation_config.data_transformation_object_file_path
            )
            return data_transformation_artifact
            
        except Exception as e:
            raise NetworkSecurityException(e,sys)
