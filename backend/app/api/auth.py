"""
认证相关 API 路由
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime

from ..database import get_db
from ..models.user import Admin
from ..schemas.user import Token, AdminLogin, AdminCreate, AdminSchema
from ..auth import (
    verify_password,
    get_password_hash,
    create_access_token,
    get_current_active_admin
)

router = APIRouter()


@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    """管理员登录"""
    result = await db.execute(
        select(Admin).where(Admin.username == form_data.username)
    )
    admin = result.scalar_one_or_none()
    
    if not admin or not verify_password(form_data.password, admin.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not admin.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="账号已被禁用"
        )
    
    # 更新最后登录时间
    admin.last_login = datetime.utcnow()
    await db.commit()
    
    # 创建访问令牌
    access_token = create_access_token(data={"sub": admin.username})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/register", response_model=AdminSchema)
async def register(
    admin_data: AdminCreate,
    db: AsyncSession = Depends(get_db),
    current_admin: Admin = Depends(get_current_active_admin)
):
    """注册新管理员（需要超级管理员权限）"""
    # 检查权限
    if current_admin.role != "super_admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有超级管理员才能创建新管理员"
        )
    
    # 检查用户名是否已存在
    result = await db.execute(
        select(Admin).where(Admin.username == admin_data.username)
    )
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户名已存在"
        )
    
    # 创建新管理员
    new_admin = Admin(
        username=admin_data.username,
        password_hash=get_password_hash(admin_data.password),
        role=admin_data.role,
        telegram_id=admin_data.telegram_id
    )
    db.add(new_admin)
    await db.commit()
    await db.refresh(new_admin)
    
    return new_admin


@router.get("/me", response_model=AdminSchema)
async def get_current_user(
    current_admin: Admin = Depends(get_current_active_admin)
):
    """获取当前登录管理员信息"""
    return current_admin
