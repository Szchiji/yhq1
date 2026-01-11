"""
提交记录相关数据模型
"""
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Enum as SQLEnum, JSON, BigInteger
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from ..database import Base


class SubmissionStatus(str, enum.Enum):
    """提交状态枚举"""
    PENDING = "pending"  # 待审核
    APPROVED = "approved"  # 已通过
    REJECTED = "rejected"  # 已拒绝
    REPLIED = "replied"  # 已回复


class Submission(Base):
    """用户提交记录模型"""
    __tablename__ = "submissions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, comment="用户ID")
    flow_id = Column(Integer, ForeignKey("flows.id"), nullable=False, comment="流程ID")
    status = Column(SQLEnum(SubmissionStatus), default=SubmissionStatus.PENDING, comment="审核状态")
    admin_id = Column(Integer, ForeignKey("admins.id"), nullable=True, comment="处理管理员ID")
    admin_note = Column(Text, nullable=True, comment="管理员备注")
    reply_message = Column(Text, nullable=True, comment="回复消息")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), comment="更新时间")
    processed_at = Column(DateTime(timezone=True), nullable=True, comment="处理时间")
    
    # 关系
    answers = relationship("SubmissionAnswer", back_populates="submission", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Submission {self.id}>"


class SubmissionAnswer(Base):
    """提交答案模型"""
    __tablename__ = "submission_answers"
    
    id = Column(Integer, primary_key=True, index=True)
    submission_id = Column(Integer, ForeignKey("submissions.id", ondelete="CASCADE"), nullable=False, comment="提交ID")
    step_id = Column(Integer, ForeignKey("flow_steps.id"), nullable=False, comment="步骤ID")
    question = Column(Text, nullable=False, comment="问题内容")
    answer = Column(Text, nullable=False, comment="用户答案")
    file_id = Column(String(500), nullable=True, comment="文件ID(如果是文件/图片)")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    
    # 关系
    submission = relationship("Submission", back_populates="answers")
    
    def __repr__(self):
        return f"<SubmissionAnswer {self.id}>"
