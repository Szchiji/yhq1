"""
消息模板数据模型
"""
from sqlalchemy import Column, Integer, String, DateTime, Text, Enum as SQLEnum
from sqlalchemy.sql import func
import enum
from ..database import Base


class TemplateType(str, enum.Enum):
    """模板类型枚举"""
    WELCOME = "welcome"  # 欢迎消息
    SUBMISSION_SUCCESS = "submission_success"  # 提交成功
    APPROVED = "approved"  # 审核通过
    REJECTED = "rejected"  # 审核拒绝
    ADMIN_NOTIFICATION = "admin_notification"  # 管理员通知


class MessageTemplate(Base):
    """消息模板模型"""
    __tablename__ = "message_templates"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, comment="模板名称")
    template_type = Column(SQLEnum(TemplateType), nullable=False, unique=True, comment="模板类型")
    content = Column(Text, nullable=False, comment="模板内容")
    language = Column(String(10), default="zh_cn", comment="语言")
    variables = Column(Text, nullable=True, comment="可用变量说明")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), comment="更新时间")
    
    def __repr__(self):
        return f"<MessageTemplate {self.name}>"
