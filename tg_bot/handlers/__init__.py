from aiogram import Router

from .start import router as start_router
from .expenses import router as expenses_router
from .reports import router as reports_router

# Главный роутер
router = Router()
router.include_router(start_router)
router.include_router(expenses_router)
router.include_router(reports_router)