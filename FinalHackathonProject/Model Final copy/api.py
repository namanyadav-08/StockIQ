from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import numpy as np
import os
from main import main as predict_next

MODEL_PATHS = {
    'AAPL': './models/Aapl.keras',
    'GOOG': './models/Goog.keras',
    'AMZN': './models/Amzn.keras',
    'TSLA': './models/Tsla.keras',
    'NVDA': './models/Nvda.keras',
    'META': './models/Meta.keras',
}

app = FastAPI()

class PredictRequest(BaseModel):
    symbol: str
    last_50_prices: list

class PredictResponse(BaseModel):
    predicted_prices: list

@app.post('/predict', response_model=PredictResponse)
def predict(request: PredictRequest):
    symbol = request.symbol.upper()
    if symbol not in MODEL_PATHS:
        raise HTTPException(status_code=400, detail='Unsupported stock symbol')
    model_path = MODEL_PATHS[symbol]
    if not os.path.exists(model_path):
        raise HTTPException(status_code=404, detail='Model file not found')
    last_50 = np.array(request.last_50_prices).reshape(-1, 1)
    if last_50.shape[0] != 50:
        raise HTTPException(status_code=400, detail='last_50_prices must have 50 values')
    preds = []
    last50 = last_50.flatten().tolist()
    for _ in range(5):
        arr = np.array(last50[-50:]).reshape(-1, 1)
        pred = predict_next(model=model_path, array=arr)
        if hasattr(pred, '__len__') and not isinstance(pred, str):
            pred = float(pred[0])
        else:
            pred = float(pred)
        preds.append(pred)
        last50.append(pred)
    return PredictResponse(predicted_prices=preds) 