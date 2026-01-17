"""
流程相关数据模型
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, Enum as SQLEnum, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from ..database import Base


class StepType(str, enum.Enum):
    """步骤类型枚举"""
    TEXT = "text"  # 文本输入
    SINGLE_CHOICE = "single_choice"  # 单选
    MULTIPLE_CHOICE = "multiple_choice"  # 多选
    IMAGE = "image"  # 图片上传
    FILE = "file"  # 文件上传


class Flow(Base):
    """对话流程模型"""
    __tablename__ = "flows"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, comment="流程名称")
    description = Column(Text, nullable=True, comment="流程描述")
    is_active = Column(Boolean, default=True, comment="是否激活")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), comment="更新时间")
    
    # 关系
    steps = relationship("FlowStep", back_populates="flow", cascade="all, delete-orphan", order_by="FlowStep.order")
    
    def __repr__(self):
        return f"<Flow {self.name}>"


class FlowStep(Base):
    """流程步骤模型"""
    __tablename__ = "flow_steps"
    
    id = Column(Integer, primary_key=True, index=True)
    flow_id = Column(Integer, ForeignKey("flows.id", ondelete="CASCADE"), nullable=False, comment="所属流程ID")
    order = Column(Integer, default=0, comment="步骤顺序")
    question = Column(Text, nullable=False, comment="问题内容")
    step_type = Column(SQLEnum(StepType), nullable=False, comment="步骤类型")
    options = Column(JSON, nullable=True, comment="选项列表(用于选择类型)")
    is_required = Column(Boolean, default=True, comment="是否必填")
    validation_rule = Column(String(500), nullable=True, comment="验证规则")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    
    # 关系
    flow = relationship("Flow", back_populates="steps")
    
    def __repr__(self):
        return f"<FlowStep {self.question[:30]}>"
