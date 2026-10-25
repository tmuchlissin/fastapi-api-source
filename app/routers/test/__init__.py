from fastapi import APIRouter
from . import auth, bodies, methods, read

router = APIRouter(prefix="/api/test", tags=["Test API Practice"])
router.include_router(read.router)
router.include_router(methods.router)
router.include_router(bodies.router)
router.include_router(auth.router)
