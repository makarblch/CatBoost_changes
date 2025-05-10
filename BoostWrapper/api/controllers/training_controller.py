from fastapi import APIRouter, HTTPException
from api.models.schemas import TrainInput, PredictInput
from api.services.training_service import submit_training_task, get_task_status, predict_from_latest

router = APIRouter()

@router.post("/train")
def train(input_data: TrainInput):
    try:
        task_id = submit_training_task(input_data)
        return {"message": "Training started", "task_id": task_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/info/{task_id}")
def get_info(task_id: str):
    status, model_base64 = get_task_status(task_id)
    return {"status": status, "model_base64": model_base64}

@router.post("/predict")
def predict(input_data: PredictInput):
    try:
        preds = predict_from_latest(input_data.X)
        return {"predictions": preds.tolist()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
