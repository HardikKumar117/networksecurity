import yaml
import dill
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
import os,sys
import numpy as np
import pickle

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

    

