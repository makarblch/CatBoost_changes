from api.models.db import SessionLocal, TaskModel

def get_model_by_task_id(task_id: str):
    db = SessionLocal()
    try:
        return db.query(TaskModel).filter(TaskModel.task_id == task_id).first()
    except Exception:
        print("Pussy")
    finally:
        db.close()
