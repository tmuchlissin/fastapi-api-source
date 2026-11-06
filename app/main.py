from app.routers.embedding import router as embedding_router
from app.routers.root import router as root_router
from app.routers.test import router as test_router
from app.services.embedding_service import embedding_service
from contextlib import asynccontextmanager
from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI):
    embedding_service.load_model()
    yield
    embedding_service.unload_model()


app = FastAPI(
    title="FastAPI API Source",
    description="FastAPI API Source & Local GPU Embedding Service",
    lifespan=lifespan,
)


app.include_router(root_router)
app.include_router(embedding_router)
app.include_router(test_router)


