from fastapi import FastAPI
from app.routers.root import router as root_router   
from app.routers.test import router as test_router

app = FastAPI(
    title="FastAPI API Source",
    description="A simple FastAPI API Source application"
)


app.include_router(root_router)
app.include_router(test_router)

