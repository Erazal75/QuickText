import pickle
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
import logging
from contextlib import asynccontextmanager
import asyncio

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

model = None

feature_names = ["SepalLengthCm", "SepalWidthCm", "PetalLengthCm", "PetalWidthCm"]

@asynccontextmanager
async def lifespan(app: FastAPI):
    global model
    #raise Exception("Sorry, no numbers below zero")
    # Charger le modèle entraîné
    #print("azeaeazezaeazze")
    async def load_model():
        with open('/app/JupiterNoteBook/Gaussian Process_model.sav', "rb") as f:
            return pickle.load(f)
    model = await asyncio.to_thread(load_model)
    # X = np.array([[6.0, 3.3, 3.2, 2.0]])
    # data = pd.DataFrame(X, columns=feature_names)
    # logger.info(f"{data}")
    # prediction = model.predict(data)
    # logger.info(f"prediction: {str(prediction[0])}")
    yield 

# Initialiser l'application FastAPI
app = FastAPI(lifespan=lifespan)

# Définir le modèle de requête
class IrisRequest(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float

# Définir l'endpoint de prédiction
@app.post("/predict")
def predict(iris: IrisRequest):
    global model
    logger.info(f"Received request: {iris}")    
    X = np.array([[iris.sepal_length, iris.sepal_width, iris.petal_length, iris.petal_width]])
    data = pd.DataFrame(X, columns=feature_names)
    logger.info(f"{data}")
    prediction = model.predict(data)
    logger.info(f"prediction: {str(prediction[0])}")
    return {"prediction": str(prediction[0])}
