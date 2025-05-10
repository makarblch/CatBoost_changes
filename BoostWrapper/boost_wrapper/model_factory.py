from catboost import CatBoostClassifier, CatBoostRegressor
from xgboost import XGBClassifier, XGBRegressor
from lightgbm import LGBMClassifier, LGBMRegressor

def create_model(backend: str, task: str, params: dict):
    if backend == 'catboost':
        return CatBoostClassifier(**params) if task == 'classification' else CatBoostRegressor(**params)
    elif backend == 'xgboost':
        return XGBClassifier(**params) if task == 'classification' else XGBRegressor(**params)
    elif backend == 'lightgbm':
        return LGBMClassifier(**params) if task == 'classification' else LGBMRegressor(**params)
    else:
        raise ValueError(f"Unsupported backend: {backend}")
