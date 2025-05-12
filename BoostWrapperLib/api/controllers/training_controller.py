from fastapi import APIRouter, HTTPException
from api.models.schemas import TrainInput
from api.services.training_service import submit_training_task, get_task_status

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
    status, model_base64_or_error = get_task_status(task_id)
    return {"status": status, "details": model_base64_or_error}
