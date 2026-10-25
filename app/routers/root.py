from fastapi import APIRouter

router = APIRouter(tags=["System"])

@router.get("/")
async def root():
    return {"message": "Welcome to FastAPI home! ✅"}

@router.get("/health")
async def health():
    return {"message": "Health check success ✅"}