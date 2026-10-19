from fastapi import APIRouter

router = APIRouter(tags=["System"])

@router.get("/")
async def root():
    return {"message": "Welcome to the FastAPI API Source! ✅"}

@router.get("/health-check")
async def health_check():
    return {"status": "healthy"}