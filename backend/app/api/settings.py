"""
系统设置 API 路由
"""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from ..models.user import Admin
from ..auth import get_current_active_admin
from ..config import settings

router = APIRouter()


@router.get("/")
async def get_settings(
    db: AsyncSession = Depends(get_db),
    current_admin: Admin = Depends(get_current_active_admin)
):
    """获取系统设置"""
    return {
        "app_name": settings.APP_NAME,
        "admin_chat_ids": settings.ADMIN_CHAT_IDS,
        "max_file_size": settings.MAX_FILE_SIZE,
        "cors_origins": settings.CORS_ORIGINS
    }


@router.get("/info")
async def get_system_info(
    current_admin: Admin = Depends(get_current_active_admin)
):
    """获取系统信息"""
    return {
        "version": "1.0.0",
        "app_name": settings.APP_NAME
    }
