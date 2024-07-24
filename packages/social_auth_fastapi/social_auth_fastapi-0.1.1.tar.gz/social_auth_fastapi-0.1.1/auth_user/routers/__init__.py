from fastapi import APIRouter

from ..routers.auth import auth_router
from ..routers.user import user_router
from conf import settings
from ..routers.social import social_router

router = APIRouter(prefix=settings.API_V1_STR)
router.include_router(social_router)
router.include_router(auth_router)
router.include_router(user_router)
