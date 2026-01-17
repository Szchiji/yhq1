"""
消息模板相关 Pydantic Schemas
"""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from ..models.template import TemplateType


class MessageTemplateBase(BaseModel):
    """消息模板基础 Schema"""
    name: str = Field(..., max_length=255)
    template_type: TemplateType
    content: str
    language: str = "zh_cn"
    variables: Optional[str] = None


class MessageTemplateCreate(MessageTemplateBase):
    """创建消息模板 Schema"""
    pass


class MessageTemplateUpdate(BaseModel):
    """更新消息模板 Schema"""
    name: Optional[str] = None
    content: Optional[str] = None
    language: Optional[str] = None
    variables: Optional[str] = None


class MessageTemplateSchema(MessageTemplateBase):
    """消息模板 Schema"""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
