from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
import numpy as np
import pickle, base64

from api.services.model_service import get_model_by_task_id

router = APIRouter()


class PredictRequest(BaseModel):
    task_id: str
    X: List[List[float]]


@router.post("/predict")
def predict(input_data: PredictRequest):
    try:
        model_data = get_model_by_task_id(input_data.task_id)
        if not model_data:
            raise HTTPException(status_code=404, detail="Task ID not found.")
        if model_data.status != "done":
            raise HTTPException(status_code=400, detail=f"Model not ready. Status: {model_data.status}")

        # Десериализуем модель
        model = pickle.loads(base64.b64decode(model_data.model_base64))
        preds = model.predict(np.array(input_data.X))
        return {"predictions": preds.tolist()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
