import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
import logging

from starlette.staticfiles import StaticFiles

from api.api_v1.router import api_v1_router
from core.config import settings
from core.db import app_lifespan

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=app_lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

logging.basicConfig(
    level=logging.INFO,  # Set the logging level to INFO or any other desired level
    format='%(asctime)s - %(levelname)s - %(message)s'  # Specify the logging format
)

app.mount('/static', StaticFiles(directory='static'), name='static')

app.include_router(api_v1_router)

if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)
