"""
用户相关数据模型
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum as SQLEnum, BigInteger
from sqlalchemy.sql import func
from datetime import datetime
import enum
from ..database import Base


class UserLanguage(str, enum.Enum):
    """用户语言枚举"""
    ZH_CN = "zh_cn"  # 简体中文
    ZH_TW = "zh_tw"  # 繁体中文
    EN = "en"  # English


class User(Base):
    """Telegram 用户模型"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(BigInteger, unique=True, nullable=False, index=True, comment="Telegram用户ID")
    username = Column(String(255), nullable=True, comment="Telegram用户名")
    first_name = Column(String(255), nullable=True, comment="名字")
    last_name = Column(String(255), nullable=True, comment="姓氏")
    language = Column(SQLEnum(UserLanguage), default=UserLanguage.ZH_CN, comment="语言")
    is_blocked = Column(Boolean, default=False, comment="是否被拉黑")
    is_active = Column(Boolean, default=True, comment="是否活跃")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), comment="更新时间")
    
    def __repr__(self):
        return f"<User {self.telegram_id}>"


class AdminRole(str, enum.Enum):
    """管理员角色枚举"""
    SUPER_ADMIN = "super_admin"  # 超级管理员
    ADMIN = "admin"  # 管理员
    MODERATOR = "moderator"  # 审核员
    SUPPORT = "support"  # 客服


class Admin(Base):
    """管理员模型"""
    __tablename__ = "admins"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, nullable=False, index=True, comment="用户名")
    password_hash = Column(String(255), nullable=False, comment="密码哈希")
    role = Column(SQLEnum(AdminRole), default=AdminRole.MODERATOR, comment="角色")
    is_active = Column(Boolean, default=True, comment="是否激活")
    telegram_id = Column(BigInteger, nullable=True, unique=True, comment="关联的Telegram ID")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), comment="更新时间")
    last_login = Column(DateTime(timezone=True), nullable=True, comment="最后登录时间")
    
    def __repr__(self):
        return f"<Admin {self.username}>"
