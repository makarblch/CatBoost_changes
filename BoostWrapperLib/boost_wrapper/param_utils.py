param_map = {
    'n_estimators': ('iterations', 'n_estimators', 'n_estimators'),
    'learning_rate': ('learning_rate', 'learning_rate', 'learning_rate'),
    'max_depth': ('depth', 'max_depth', 'max_depth'),

}

def translate_params(backend: str, raw_params: dict) -> dict:
    translated = {}
    for common_name, backend_keys in param_map.items():
        if common_name in raw_params:
            key = {
                'catboost': backend_keys[0],
                'xgboost': backend_keys[1],
                'lightgbm': backend_keys[2],
            }.get(backend)
            if key:
                translated[key] = raw_params[common_name]
    return translated
