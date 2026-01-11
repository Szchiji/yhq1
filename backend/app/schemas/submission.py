"""
提交记录相关 Pydantic Schemas
"""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from ..models.submission import SubmissionStatus


class SubmissionAnswerSchema(BaseModel):
    """提交答案 Schema"""
    id: int
    submission_id: int
    step_id: int
    question: str
    answer: str
    file_id: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


class SubmissionSchema(BaseModel):
    """提交记录 Schema"""
    id: int
    user_id: int
    flow_id: int
    status: SubmissionStatus
    admin_id: Optional[int] = None
    admin_note: Optional[str] = None
    reply_message: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    processed_at: Optional[datetime] = None
    answers: List[SubmissionAnswerSchema] = []
    
    class Config:
        from_attributes = True


class SubmissionUpdate(BaseModel):
    """更新提交记录 Schema"""
    status: Optional[SubmissionStatus] = None
    admin_note: Optional[str] = None
    reply_message: Optional[str] = None
