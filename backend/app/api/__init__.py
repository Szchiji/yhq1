# API 路由包初始化
from fastapi import APIRouter
from .auth import router as auth_router
from .dashboard import router as dashboard_router
from .menus import router as menus_router
from .flows import router as flows_router
from .templates import router as templates_router
from .submissions import router as submissions_router
from .users import router as users_router
from .settings import router as settings_router

api_router = APIRouter()

# 注册所有路由
api_router.include_router(auth_router, prefix="/auth", tags=["认证"])
api_router.include_router(dashboard_router, prefix="/dashboard", tags=["仪表盘"])
api_router.include_router(menus_router, prefix="/menus", tags=["菜单管理"])
api_router.include_router(flows_router, prefix="/flows", tags=["流程管理"])
api_router.include_router(templates_router, prefix="/templates", tags=["模板管理"])
api_router.include_router(submissions_router, prefix="/submissions", tags=["审核管理"])
api_router.include_router(users_router, prefix="/users", tags=["用户管理"])
api_router.include_router(settings_router, prefix="/settings", tags=["系统设置"])

__all__ = ["api_router"]
