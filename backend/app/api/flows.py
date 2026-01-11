"""
流程管理 API 路由
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from typing import List

from ..database import get_db
from ..models.flow import Flow, FlowStep
from ..models.user import Admin
from ..schemas.flow import FlowSchema, FlowCreate, FlowUpdate
from ..auth import get_current_active_admin

router = APIRouter()


@router.get("/", response_model=List[FlowSchema])
async def list_flows(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_admin: Admin = Depends(get_current_active_admin)
):
    """获取流程列表"""
    result = await db.execute(
        select(Flow)
        .options(selectinload(Flow.steps))
        .offset(skip)
        .limit(limit)
    )
    flows = result.scalars().all()
    return flows


@router.post("/", response_model=FlowSchema)
async def create_flow(
    flow_data: FlowCreate,
    db: AsyncSession = Depends(get_db),
    current_admin: Admin = Depends(get_current_active_admin)
):
    """创建新流程"""
    # 创建流程
    flow = Flow(
        name=flow_data.name,
        description=flow_data.description,
        is_active=flow_data.is_active
    )
    db.add(flow)
    await db.flush()  # 获取 flow.id
    
    # 创建步骤
    for step_data in flow_data.steps:
        step = FlowStep(
            flow_id=flow.id,
            **step_data.model_dump()
        )
        db.add(step)
    
    await db.commit()
    await db.refresh(flow)
    
    # 重新加载包含步骤的流程
    result = await db.execute(
        select(Flow)
        .options(selectinload(Flow.steps))
        .where(Flow.id == flow.id)
    )
    flow = result.scalar_one()
    return flow


@router.get("/{flow_id}", response_model=FlowSchema)
async def get_flow(
    flow_id: int,
    db: AsyncSession = Depends(get_db),
    current_admin: Admin = Depends(get_current_active_admin)
):
    """获取流程详情"""
    result = await db.execute(
        select(Flow)
        .options(selectinload(Flow.steps))
        .where(Flow.id == flow_id)
    )
    flow = result.scalar_one_or_none()
    if not flow:
        raise HTTPException(status_code=404, detail="流程不存在")
    return flow


@router.put("/{flow_id}", response_model=FlowSchema)
async def update_flow(
    flow_id: int,
    flow_data: FlowUpdate,
    db: AsyncSession = Depends(get_db),
    current_admin: Admin = Depends(get_current_active_admin)
):
    """更新流程"""
    result = await db.execute(
        select(Flow)
        .options(selectinload(Flow.steps))
        .where(Flow.id == flow_id)
    )
    flow = result.scalar_one_or_none()
    if not flow:
        raise HTTPException(status_code=404, detail="流程不存在")
    
    update_data = flow_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(flow, key, value)
    
    await db.commit()
    await db.refresh(flow)
    return flow


@router.delete("/{flow_id}")
async def delete_flow(
    flow_id: int,
    db: AsyncSession = Depends(get_db),
    current_admin: Admin = Depends(get_current_active_admin)
):
    """删除流程"""
    result = await db.execute(select(Flow).where(Flow.id == flow_id))
    flow = result.scalar_one_or_none()
    if not flow:
        raise HTTPException(status_code=404, detail="流程不存在")
    
    await db.delete(flow)
    await db.commit()
    return {"message": "流程已删除"}
