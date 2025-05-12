from sklearn.base import BaseEstimator
from .param_utils import translate_params
from .logger import get_logger
from .model_factory import create_model

class BoostWrapper(BaseEstimator):
    """
    Универсальный wrapper над CatBoost, XGBoost и LightGBM.
    Drop-in совместим с их API.
    """
    def __init__(self, backend='catboost', task='classification', **params):
        self.backend = backend.lower()
        self.task = task.lower()
        self.raw_params = params
        self._model = None
        self.logger = get_logger()
        self._init_model()

    def _init_model(self):
        translated = translate_params(self.backend, self.raw_params)
        self._model = create_model(self.backend, self.task, translated)
        self.logger.info(f"Initialized {self.backend} model with params: {translated}")

    def fit(self, X, y, **kwargs):
        return self._model.fit(X, y, **kwargs)

    def predict(self, X):
        return self._model.predict(X)

    def predict_proba(self, X):
        if hasattr(self._model, 'predict_proba'):
            return self._model.predict_proba(X)
        raise NotImplementedError("predict_proba not implemented")

    def get_params(self, deep=True):
        return {'backend': self.backend, 'task': self.task, **self.raw_params}

    def set_params(self, **params):
        for key, val in params.items():
            if key in ['backend', 'task']:
                setattr(self, key, val)
            else:
                self.raw_params[key] = val
        self._init_model()
        return self
