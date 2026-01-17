"""
菜单管理 API 路由
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from ..database import get_db
from ..models.menu import Menu
from ..models.user import Admin
from ..schemas.menu import MenuSchema, MenuCreate, MenuUpdate
from ..auth import get_current_active_admin

router = APIRouter()


@router.get("/", response_model=List[MenuSchema])
async def list_menus(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_admin: Admin = Depends(get_current_active_admin)
):
    """获取菜单列表"""
    result = await db.execute(
        select(Menu).order_by(Menu.order).offset(skip).limit(limit)
    )
    menus = result.scalars().all()
    return menus


@router.post("/", response_model=MenuSchema)
async def create_menu(
    menu_data: MenuCreate,
    db: AsyncSession = Depends(get_db),
    current_admin: Admin = Depends(get_current_active_admin)
):
    """创建新菜单"""
    menu = Menu(**menu_data.model_dump())
    db.add(menu)
    await db.commit()
    await db.refresh(menu)
    return menu


@router.get("/{menu_id}", response_model=MenuSchema)
async def get_menu(
    menu_id: int,
    db: AsyncSession = Depends(get_db),
    current_admin: Admin = Depends(get_current_active_admin)
):
    """获取菜单详情"""
    result = await db.execute(select(Menu).where(Menu.id == menu_id))
    menu = result.scalar_one_or_none()
    if not menu:
        raise HTTPException(status_code=404, detail="菜单不存在")
    return menu


@router.put("/{menu_id}", response_model=MenuSchema)
async def update_menu(
    menu_id: int,
    menu_data: MenuUpdate,
    db: AsyncSession = Depends(get_db),
    current_admin: Admin = Depends(get_current_active_admin)
):
    """更新菜单"""
    result = await db.execute(select(Menu).where(Menu.id == menu_id))
    menu = result.scalar_one_or_none()
    if not menu:
        raise HTTPException(status_code=404, detail="菜单不存在")
    
    update_data = menu_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(menu, key, value)
    
    await db.commit()
    await db.refresh(menu)
    return menu


@router.delete("/{menu_id}")
async def delete_menu(
    menu_id: int,
    db: AsyncSession = Depends(get_db),
    current_admin: Admin = Depends(get_current_active_admin)
):
    """删除菜单"""
    result = await db.execute(select(Menu).where(Menu.id == menu_id))
    menu = result.scalar_one_or_none()
    if not menu:
        raise HTTPException(status_code=404, detail="菜单不存在")
    
    await db.delete(menu)
    await db.commit()
    return {"message": "菜单已删除"}
