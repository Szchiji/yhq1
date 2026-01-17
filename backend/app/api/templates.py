"""
消息模板管理 API 路由
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from ..database import get_db
from ..models.template import MessageTemplate
from ..models.user import Admin
from ..schemas.template import MessageTemplateSchema, MessageTemplateCreate, MessageTemplateUpdate
from ..auth import get_current_active_admin

router = APIRouter()


@router.get("/", response_model=List[MessageTemplateSchema])
async def list_templates(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_admin: Admin = Depends(get_current_active_admin)
):
    """获取模板列表"""
    result = await db.execute(
        select(MessageTemplate).offset(skip).limit(limit)
    )
    templates = result.scalars().all()
    return templates


@router.post("/", response_model=MessageTemplateSchema)
async def create_template(
    template_data: MessageTemplateCreate,
    db: AsyncSession = Depends(get_db),
    current_admin: Admin = Depends(get_current_active_admin)
):
    """创建新模板"""
    # 检查模板类型是否已存在
    result = await db.execute(
        select(MessageTemplate).where(
            MessageTemplate.template_type == template_data.template_type
        )
    )
    existing = result.scalar_one_or_none()
    if existing:
        raise HTTPException(status_code=400, detail="该模板类型已存在")
    
    template = MessageTemplate(**template_data.model_dump())
    db.add(template)
    await db.commit()
    await db.refresh(template)
    return template


@router.get("/{template_id}", response_model=MessageTemplateSchema)
async def get_template(
    template_id: int,
    db: AsyncSession = Depends(get_db),
    current_admin: Admin = Depends(get_current_active_admin)
):
    """获取模板详情"""
    result = await db.execute(
        select(MessageTemplate).where(MessageTemplate.id == template_id)
    )
    template = result.scalar_one_or_none()
    if not template:
        raise HTTPException(status_code=404, detail="模板不存在")
    return template


@router.put("/{template_id}", response_model=MessageTemplateSchema)
async def update_template(
    template_id: int,
    template_data: MessageTemplateUpdate,
    db: AsyncSession = Depends(get_db),
    current_admin: Admin = Depends(get_current_active_admin)
):
    """更新模板"""
    result = await db.execute(
        select(MessageTemplate).where(MessageTemplate.id == template_id)
    )
    template = result.scalar_one_or_none()
    if not template:
        raise HTTPException(status_code=404, detail="模板不存在")
    
    update_data = template_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(template, key, value)
    
    await db.commit()
    await db.refresh(template)
    return template


@router.delete("/{template_id}")
async def delete_template(
    template_id: int,
    db: AsyncSession = Depends(get_db),
    current_admin: Admin = Depends(get_current_active_admin)
):
    """删除模板"""
    result = await db.execute(
        select(MessageTemplate).where(MessageTemplate.id == template_id)
    )
    template = result.scalar_one_or_none()
    if not template:
        raise HTTPException(status_code=404, detail="模板不存在")
    
    await db.delete(template)
    await db.commit()
    return {"message": "模板已删除"}
