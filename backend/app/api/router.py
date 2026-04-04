from fastapi import APIRouter

from app.api.routes.admin import router as admin_router
from app.api.routes.health import router as health_router
from app.api.routes.test_flow import router as test_router


api_router = APIRouter()
api_router.include_router(health_router, tags=["health"])
api_router.include_router(admin_router, prefix="/admin", tags=["admin"])
api_router.include_router(test_router, prefix="/test", tags=["test"])
