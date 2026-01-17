"""
菜单相关 Pydantic Schemas
"""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class MenuBase(BaseModel):
    """菜单基础 Schema"""
    name: str = Field(..., max_length=255)
    icon: Optional[str] = Field(None, max_length=50)
    order: int = 0
    flow_id: Optional[int] = None
    buttons_per_row: int = Field(2, ge=1, le=4)
    description: Optional[str] = None


class MenuCreate(MenuBase):
    """创建菜单 Schema"""
    is_active: bool = True


class MenuUpdate(BaseModel):
    """更新菜单 Schema"""
    name: Optional[str] = None
    icon: Optional[str] = None
    order: Optional[int] = None
    flow_id: Optional[int] = None
    is_active: Optional[bool] = None
    buttons_per_row: Optional[int] = None
    description: Optional[str] = None


class MenuSchema(MenuBase):
    """菜单 Schema"""
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
