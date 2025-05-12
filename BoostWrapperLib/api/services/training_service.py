from api.models.training_task import TrainingTask, TaskStatus
from api.models.schemas import TrainInput
from boost_wrapper import BoostWrapper
from api.models.db import SessionLocal, TaskModel
import uuid, threading, base64, pickle
import numpy as np

tasks = {}

def submit_training_task(train_input: TrainInput) -> str:
    task_id = str(uuid.uuid4())
    task = TrainingTask(task_id)
    tasks[task_id] = task

    def run():
        db = SessionLocal()
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

            # Сериализуем модель
            model_binary = pickle.dumps(model)
            model_base64 = (
                base64.b64encode(model_binary).decode('utf-8')
                if len(model_binary) <= 30 * 1024 * 1024
                else None
            )

            # Проверяем, есть ли уже такая запись
            db_task = db.query(TaskModel).filter_by(task_id=task_id).first()
            if not db_task:
                db_task = TaskModel(task_id=task_id)

            db_task.status = "done"
            db_task.model_base64 = model_base64
            db_task.error_message = None

            db.add(db_task)
            db.commit()

        except Exception as e:
            task.status = TaskStatus.FAILED
            task.error = str(e)

            db_task = db.query(TaskModel).filter_by(task_id=task_id).first()
            if not db_task:
                db_task = TaskModel(task_id=task_id)

            db_task.status = "failed"
            db_task.error_message = str(e)
            db_task.model_base64 = None

            db.add(db_task)
            db.commit()

        finally:
            db.close()

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
