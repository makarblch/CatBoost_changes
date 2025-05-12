from pydantic import BaseModel, Field
from typing import List, Literal


class TrainInput(BaseModel):
    X: List[List[float]]
    y: List[float]
    backend: Literal['catboost', 'xgboost', 'lightgbm']
    task: Literal['classification', 'regression']
    params: dict = Field(default_factory=dict)


class PredictByIdInput(BaseModel):
    task_id: str
    X: List[List[float]]
