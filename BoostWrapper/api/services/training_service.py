import uuid
import threading
import base64
import pickle
import numpy as np
from api.models.training_task import TrainingTask, TaskStatus
from api.models.schemas import TrainInput
from boost_wrapper import BoostWrapper

# Состояние всех задач
tasks = {}
latest_model = None

def submit_training_task(train_input: TrainInput) -> str:
    task_id = str(uuid.uuid4())
    task = TrainingTask(task_id)
    tasks[task_id] = task

    def run():
        try:
            task.status = TaskStatus.RUNNING
            model = BoostWrapper(
                backend=train_input.backend,
                task=train_input.task,
                **train_input.params
            )
            model.fit(np.array(train_input.X), np.array(train_input.y))
            task.model = model
            task.status = TaskStatus.DONE
            global latest_model
            latest_model = model
        except Exception as e:
            task.status = TaskStatus.FAILED
            task.error = str(e)

    threading.Thread(target=run, daemon=True).start()
    return task_id

def get_task_status(task_id: str):
    task = tasks.get(task_id)
    if not task:
        return "not_found", None

    if task.status == TaskStatus.DONE:
        serialized = base64.b64encode(pickle.dumps(task.model)).decode('utf-8')
        return task.status, serialized
    elif task.status == TaskStatus.FAILED:
        return task.status, task.error
    else:
        return task.status, None

def predict_from_latest(X: list):
    if latest_model is None:
        raise Exception("No trained model available")
    return latest_model.predict(np.array(X))
