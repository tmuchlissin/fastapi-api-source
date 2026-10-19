from fastapi import FastAPI
from app.routers.root import router as root_router
from app.routers.test.items import router as test_items_router

app = FastAPI(
    title="FastAPI API Source",
    description="A simple FastAPI application for demonstrating API functionality.",
)

app.include_router(root_router)
app.include_router(test_items_router)