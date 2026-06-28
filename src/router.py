from fastapi import APIRouter

from src.config import settings
from src.api.service import router as api_router


router = APIRouter(prefix=settings.api.prefix)
router.include_router(api_router)
