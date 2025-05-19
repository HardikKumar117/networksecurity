import os,sys
import certifi
from dotenv import load_dotenv
ca=certifi.where()
load_dotenv()
mongo_db_url=os.getenv("MONGO_DB_URL")
print(mongo_db_url)

import pymongo
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.pipeline.training_pipeline import TrainingPipeline
from networksecurity.util.ml_utils.model.estimator import NetworkModel

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI,File,UploadFile,Request
from uvicorn import run as app_run
from fastapi.responses import Response
from starlette.responses import RedirectResponse
import pandas as pd
from networksecurity.util.main_utils.utils import load_object

client=pymongo.MongoClient(mongo_db_url,tlsCAFile=ca)
from networksecurity.constant.training_pipeline import DATA_INGESTION_DATABASE_NAME
from networksecurity.constant.training_pipeline import DATA_INGESTION_COLLECTION_NAME
collection= client[DATA_INGESTION_COLLECTION_NAME]
database=client[DATA_INGESTION_DATABASE_NAME]

app=FastAPI()
origins=["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
from fastapi.templating import Jinja2Templates
templates=Jinja2Templates(directory="./templates")

@app.get("/",tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")
@app.get("/train")
async def train_data():
    try:
        training_pipeline=TrainingPipeline()
        training_pipeline.start_pipeline()
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    
@app.post("/predict")
async def predict_data(request:Request,file:UploadFile=File(...)):
    try:
        df=pd.read_csv(file.file)
        # Drop the Unnamed: 0 column if it exists
        if 'Unnamed: 0' in df.columns:
            df = df.drop('Unnamed: 0', axis=1)
        preprocessor=load_object("final_models\preprocessor.pkl")
        model=load_object("final_models\model.pkl")
        networkmodel=NetworkModel(processor=preprocessor,model=model)
        print(df.iloc[0])
        y_pred=networkmodel.predict(df)
        print(y_pred)
        df['predicted_column']=y_pred
        df.to_csv("predictionData/output.csv")
        table_html=df.to_html(classes='table table-striped')
        return templates.TemplateResponse("table.html",{'request':request,'table':table_html})
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    
if __name__== "__main__":
    app_run(app,host="localhost",port=8000)