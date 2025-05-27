from fastapi import APIRouter, UploadFile, File
from src.controller import predict_controller

router = APIRouter()

@router.post("/predict")
async def predict(file: UploadFile = File(...)):
    return await predict_controller.predict(file)

@router.get("/history")
async def get_prediction_history():
    return await predict_controller.get_prediction_history()