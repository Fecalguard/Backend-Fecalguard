from fastapi import FastAPI
from src.router.public_api import router

# Inisialisasi FastAPI
app = FastAPI()

# Menambahkan router ke app FastAPI
app.include_router(router, prefix="/api", tags=["api"])