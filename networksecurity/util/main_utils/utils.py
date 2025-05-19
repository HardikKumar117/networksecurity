import yaml
import dill
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
import os,sys
import numpy as np
import pickle
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import r2_score

def read_yaml_file(filepath:str)->dict:
    try:
        with open(filepath,'rb') as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    
def write_yaml_file(filepath:str,content:object,replace:bool=False)->None:
    try:
        if replace and os.path.exists(filepath):
            os.remove(filepath)
        os.makedirs(os.path.dirname(filepath),exist_ok=True)
        with open(filepath,"w") as yaml_file:
            yaml.dump(content,yaml_file)
    except Exception as e:
        raise NetworkSecurityException(e,sys)
def save_numpy_array_data(filepath:str,array:np.array):
    try:
        dir_name=os.path.dirname(filepath)
        os.makedirs(dir_name,exist_ok=True)
        with open(filepath,"wb") as file_obj:
            np.save(file_obj,array)
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    
def save_object(filepath:str,model:object)->None:
    try:
        dir_name=os.path.dirname(filepath)
        os.makedirs(dir_name,exist_ok=True)
        with open(filepath,"wb") as file_obj:
            pickle.dump(model,file_obj)
    except Exception as e:
        raise NetworkSecurityException(e,sys)

def load_object(filepath:str,)->object:
    try:
        if not os.path.exists(filepath):
            raise Exception(f"{filepath} does not exist")
        with open(filepath,"rb") as file_obj:
            return pickle.load(file_obj)
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    
def load_numpy_data(filepath:str,)->np.array:
    try:
        with open(filepath,'rb') as file:
            return np.load(file)
    except Exception as e:
        raise NetworkSecurityException(e,sys)
def evaluate_models(X_train,y_train,X_test,y_test,models,param):
    try:
        report={}
        for i in range(len(list(models))):
            model=list(models.values())[i]
            para=param[list(models.keys())[i]]

            gs=GridSearchCV(model,para,cv=3)
            gs.fit(X_train,y_train)
            model.set_params(**gs.best_params_)
            model.fit(X_train,y_train)
            
            y_train_pred=model.predict(X_train)
            y_test_pred=model.predict(X_test)

            train_model_score=r2_score(y_train,y_train_pred)
            test_model_score=r2_score(y_test,y_test_pred)
            report[list(models.keys())[i]]=test_model_score
            return report
    except Exception as e:
        raise NetworkSecurityException(e,sys)

    

