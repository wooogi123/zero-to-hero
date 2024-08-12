from fastapi import APIRouter

from .todos import router as todos_router

router = APIRouter()

router.include_router(router=todos_router, prefix="/todos")
