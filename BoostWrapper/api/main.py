from fastapi import FastAPI
from api.controllers import training_controller

app = FastAPI(title="BoostWrapper API")
app.include_router(training_controller.router)
