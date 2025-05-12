from fastapi import APIRouter, HTTPException
import numpy as np
import pickle
import base64

from api.models.schemas import PredictByIdInput
from api.services.model_service import get_model_by_task_id

router = APIRouter()


@router.post("/predict")
def predict(input_data: PredictByIdInput):
    try:
        model_data = get_model_by_task_id(input_data.task_id)

        if not model_data:
            raise HTTPException(status_code=404, detail="Task ID not found.")
        if model_data.status != "done":
            raise HTTPException(status_code=400, detail=f"Model not ready. Status: {model_data.status}")
        if not model_data.model_base64:
            raise HTTPException(status_code=400, detail="Trained model not found.")

        model = pickle.loads(base64.b64decode(model_data.model_base64))
        preds = model.predict(np.array(input_data.X))

        return {"predictions": preds.tolist()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")
