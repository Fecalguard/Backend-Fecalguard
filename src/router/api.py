from fastapi import APIRouter, UploadFile, File, Depends
from src.controller import predict_controller, auth_controller

router = APIRouter()

@router.post("/register")
async def register(username: str, password: str):
    return await auth_controller.register(username, password)

@router.post("/login")
async def login(username: str, password: str):
    return await auth_controller.login(username, password)

@router.post("/predict")
async def predict(
    file: UploadFile = File(...),
    current_user: dict = Depends(auth_controller.get_current_user)
):
    return await predict_controller.predict(file, current_user)

@router.get("/history")
async def get_prediction_history(
    current_user: dict = Depends(auth_controller.get_current_user)
):
    return await predict_controller.get_prediction_history(current_user)