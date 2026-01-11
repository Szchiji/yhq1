"""
流程相关 Pydantic Schemas
"""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from ..models.flow import StepType


class FlowStepBase(BaseModel):
    """流程步骤基础 Schema"""
    order: int = 0
    question: str
    step_type: StepType
    options: Optional[List[str]] = None
    is_required: bool = True
    validation_rule: Optional[str] = None


class FlowStepCreate(FlowStepBase):
    """创建流程步骤 Schema"""
    pass


class FlowStepSchema(FlowStepBase):
    """流程步骤 Schema"""
    id: int
    flow_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class FlowBase(BaseModel):
    """流程基础 Schema"""
    name: str = Field(..., max_length=255)
    description: Optional[str] = None


class FlowCreate(FlowBase):
    """创建流程 Schema"""
    is_active: bool = True
    steps: List[FlowStepCreate] = []


class FlowUpdate(BaseModel):
    """更新流程 Schema"""
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None


class FlowSchema(FlowBase):
    """流程 Schema"""
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    steps: List[FlowStepSchema] = []
    
    class Config:
        from_attributes = True
