from fastapi import FastAPI
from pydantic import BaseModel
from pathlib import Path
import pickle

MODEL_FOLDER = Path("models/")
model_wrapper_list = []

app = FastAPI(
   title="IRIS classifier",
   description="I classify flowers",
   version="0.1"
)

class FlowerData(BaseModel):
   sepal_length: float
   sepal_width: float
   petal_length: float
   petal_width: float

@app.on_event("startup")
def load_models():
   for model_path in MODEL_FOLDER.glob("*.pkl"):
      with open(model_path, "rb") as model_file:
        model_wrapper_list.append(pickle.load(model_file))

@app.get("/")
def root ():
   return {"message" : "Welcome to the IRIS classifier"}


@app.get("/models")
def getModels():
   model_list = [model["type"] for model in model_wrapper_list]
   return {"models" : model_list}

"""
# RPC style : the name of the endpoint is a verb
@app.post("/predict")
def predict(flower_data: FlowerData, model_type : str):
   return ""
"""

# RESTful style
@app.post("/models/{model_type}")
def predict(flower_data: FlowerData, model_type : str):
    for model_w in model_wrapper_list:
      if (model_w["type"] == model_type):
         model = model_w["model"]
         break
    else:
      return {
        "status-code" : 400,
        "message" : "Model not found"   
      }
    
    prediction = model.predict ([[flower_data.sepal_length, flower_data.sepal_width, 
                                  flower_data.petal_length, flower_data.petal_width]])
    return {
       "status-code" : 200,
       "message" : int(prediction[0])  # cast the NumPY object to an integer
    }