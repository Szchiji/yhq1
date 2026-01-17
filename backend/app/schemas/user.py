"""
用户相关 Pydantic Schemas
"""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from ..models.user import UserLanguage, AdminRole


class UserSchema(BaseModel):
    """用户 Schema"""
    id: int
    telegram_id: int
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    language: UserLanguage = UserLanguage.ZH_CN
    is_blocked: bool = False
    is_active: bool = True
    created_at: datetime
    
    class Config:
        from_attributes = True


class AdminSchema(BaseModel):
    """管理员 Schema"""
    id: int
    username: str
    role: AdminRole
    is_active: bool
    telegram_id: Optional[int] = None
    created_at: datetime
    last_login: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class AdminCreate(BaseModel):
    """创建管理员 Schema"""
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)
    role: AdminRole = AdminRole.MODERATOR
    telegram_id: Optional[int] = None


class AdminLogin(BaseModel):
    """管理员登录 Schema"""
    username: str
    password: str


class Token(BaseModel):
    """JWT Token Schema"""
    access_token: str
    token_type: str = "bearer"
