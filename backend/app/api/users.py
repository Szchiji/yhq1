"""
用户管理 API 路由
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List, Optional

from ..database import get_db
from ..models.user import User, Admin
from ..schemas.user import UserSchema
from ..auth import get_current_active_admin

router = APIRouter()


@router.get("/", response_model=List[UserSchema])
async def list_users(
    skip: int = 0,
    limit: int = 100,
    is_blocked: Optional[bool] = None,
    db: AsyncSession = Depends(get_db),
    current_admin: Admin = Depends(get_current_active_admin)
):
    """获取用户列表"""
    query = select(User)
    
    if is_blocked is not None:
        query = query.where(User.is_blocked == is_blocked)
    
    query = query.order_by(User.created_at.desc()).offset(skip).limit(limit)
    
    result = await db.execute(query)
    users = result.scalars().all()
    return users


@router.get("/stats")
async def get_user_stats(
    db: AsyncSession = Depends(get_db),
    current_admin: Admin = Depends(get_current_active_admin)
):
    """获取用户统计"""
    total_result = await db.execute(select(func.count(User.id)))
    total_users = total_result.scalar()
    
    active_result = await db.execute(
        select(func.count(User.id)).where(User.is_active == True)
    )
    active_users = active_result.scalar()
    
    blocked_result = await db.execute(
        select(func.count(User.id)).where(User.is_blocked == True)
    )
    blocked_users = blocked_result.scalar()
    
    return {
        "total_users": total_users,
        "active_users": active_users,
        "blocked_users": blocked_users
    }


@router.get("/{user_id}", response_model=UserSchema)
async def get_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_admin: Admin = Depends(get_current_active_admin)
):
    """获取用户详情"""
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    return user


@router.post("/{user_id}/block")
async def block_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_admin: Admin = Depends(get_current_active_admin)
):
    """拉黑用户"""
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    user.is_blocked = True
    await db.commit()
    return {"message": "用户已拉黑"}


@router.post("/{user_id}/unblock")
async def unblock_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_admin: Admin = Depends(get_current_active_admin)
):
    """解除拉黑"""
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    user.is_blocked = False
    await db.commit()
    return {"message": "已解除拉黑"}
