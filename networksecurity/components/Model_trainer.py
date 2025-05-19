from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
import os,sys
import numpy as np
from networksecurity.entity.config_entity import ModelTrainerConfig
from networksecurity.entity.artifact_entity import DataTransformationArtifact,ModelTrainerArtifact
import mlflow
from networksecurity.util.main_utils.utils import save_object,load_object,load_numpy_data,evaluate_models
from networksecurity.util.ml_utils.model.estimator import NetworkModel
from networksecurity.util.ml_utils.metric.classification_metrics import get_classification_score

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import r2_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import AdaBoostClassifier,RandomForestClassifier,GradientBoostingClassifier

import dagshub
dagshub.init(repo_owner='HardikKumar117', repo_name='networksecurity', mlflow=True)

class ModelTrainer:
    def __init__(self,model_trainer_config:ModelTrainerConfig,data_transformation_artifact:DataTransformationArtifact):
        try:
            self.model_trainer_config=model_trainer_config
            self.data_transformation_artifact=data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def track_mlflow(self,best_model,train_classification_artifact):
        with mlflow.start_run():
            f1_score=train_classification_artifact.f1_score
            precision_score=train_classification_artifact.precision_score
            recall_score=train_classification_artifact.recall_score
            
            mlflow.log_metrics({
                "f1_score":f1_score,
                "precision_score":precision_score,
                "recall_score":recall_score
            })
            mlflow.sklearn.log_model(best_model,"model")



    def train_model(self,X_train,y_train,X_test,y_test):
        models={
            "LogisticRegression":LogisticRegression(verbose=1),
            "DecisionTreeClassifier":DecisionTreeClassifier(),
            "KNeighborsClassifier":KNeighborsClassifier(),
            "AdaBoostClassifier":AdaBoostClassifier(),
            "RandomForestClassifier":RandomForestClassifier(verbose=1),
            "GradientBoostingClassifier":GradientBoostingClassifier(verbose=1)
        }

        params = {
       "LogisticRegression": {
        "C": [0.01, 0.1, 1, 10, 100],
        "solver": ['liblinear', 'lbfgs'],
        "penalty": ['l1', 'l2'],
        "max_iter": [100, 200, 500]
       },
       "DecisionTreeClassifier": {
        "criterion": ["gini", "entropy"],
        "max_depth": [None, 5, 10, 20],
        "min_samples_split": [2, 5, 10],
        "min_samples_leaf": [1, 2, 4]
      },
     "KNeighborsClassifier": {
        "n_neighbors": [3, 5, 7, 9],
        "weights": ['uniform', 'distance'],
        "metric": ['euclidean', 'manhattan', 'minkowski']
      },
       "AdaBoostClassifier": {
        "n_estimators": [50, 100, 200],
        "learning_rate": [0.01, 0.1, 1, 2]
      },
      "RandomForestClassifier": {
        "n_estimators": [100, 200, 300],
        "criterion": ["gini", "entropy"],
        "max_depth": [None, 10, 20, 30],
        "min_samples_split": [2, 5, 10],
        "min_samples_leaf": [1, 2, 4]
       },
      "GradientBoostingClassifier": {
        "n_estimators": [100, 150, 200],
        "learning_rate": [0.01, 0.1, 0.2],
        "max_depth": [3, 5, 7],
        "min_samples_split": [2, 5, 10],
        "min_samples_leaf": [1, 2, 4],
        "subsample": [0.8, 1.0]
          }
       }
        model_report=evaluate_models(X_train=X_train,y_train=y_train,X_test=X_test,y_test=y_test,models=models,param=params)
        best_model_score=max(sorted(model_report.values()))
        best_model_name=list(model_report.keys())[list(model_report.values()).index(best_model_score)]
        best_model=models[best_model_name]

        y_train_pred=best_model.predict(X_train)
        train_classification_artifact=get_classification_score(y_true=y_train,y_pred=y_train_pred)

        y_test_pred=best_model.predict(X_test)
        test_classification_artifact=get_classification_score(y_true=y_test,y_pred=y_test_pred)

        ## track the MLFlow
        self.track_mlflow(best_model,train_classification_artifact)
        self.track_mlflow(best_model,test_classification_artifact)
       
        

        preprocessor=load_object(self.data_transformation_artifact.transformed_object_file_path)
        dir_name=os.path.dirname(self.model_trainer_config.model_trainer_file_path)
        os.makedirs(dir_name,exist_ok=True)
        save_object("final_models/preprocessor.pkl",preprocessor)
        
        network_model=NetworkModel(processor=preprocessor,model=best_model)
        save_object(self.model_trainer_config.model_trainer_file_path,network_model)
        save_object("final_models/model.pkl",best_model)
        model_trainer_artifact=ModelTrainerArtifact(trained_model_file_path=self.model_trainer_config.model_trainer_file_path,
                             test_metric_artifact=train_classification_artifact,
                             trained_metric_artifact=test_classification_artifact)
        logging.info(f"the model is{model_trainer_artifact} ")
        return model_trainer_artifact

    def initiate_model_trainer(self)-> ModelTrainerArtifact:
        try:
            train_file_path=self.data_transformation_artifact.transformed_train_file_path
            test_file_path=self.data_transformation_artifact.transformed_test_file_path

            train_arr=load_numpy_data(train_file_path)
            test_arr=load_numpy_data(test_file_path)
            X_train,y_train,X_test,y_test=(
                train_arr[:,:-1],
                train_arr[:,-1],
                test_arr[:,:-1],
                test_arr[:,-1],
            )
            return self.train_model(X_train,y_train,X_test,y_test)
    
        except Exception as e:
            raise NetworkSecurityException(e,sys)



