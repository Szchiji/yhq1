"""
审核管理 API 路由
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from typing import List, Optional
from datetime import datetime

from ..database import get_db
from ..models.submission import Submission, SubmissionStatus
from ..models.user import Admin
from ..schemas.submission import SubmissionSchema, SubmissionUpdate
from ..auth import get_current_active_admin

router = APIRouter()


@router.get("/", response_model=List[SubmissionSchema])
async def list_submissions(
    skip: int = 0,
    limit: int = 100,
    status: Optional[SubmissionStatus] = None,
    db: AsyncSession = Depends(get_db),
    current_admin: Admin = Depends(get_current_active_admin)
):
    """获取提交列表"""
    query = select(Submission).options(selectinload(Submission.answers))
    
    if status:
        query = query.where(Submission.status == status)
    
    query = query.order_by(Submission.created_at.desc()).offset(skip).limit(limit)
    
    result = await db.execute(query)
    submissions = result.scalars().all()
    return submissions


@router.get("/{submission_id}", response_model=SubmissionSchema)
async def get_submission(
    submission_id: int,
    db: AsyncSession = Depends(get_db),
    current_admin: Admin = Depends(get_current_active_admin)
):
    """获取提交详情"""
    result = await db.execute(
        select(Submission)
        .options(selectinload(Submission.answers))
        .where(Submission.id == submission_id)
    )
    submission = result.scalar_one_or_none()
    if not submission:
        raise HTTPException(status_code=404, detail="提交记录不存在")
    return submission


@router.put("/{submission_id}", response_model=SubmissionSchema)
async def update_submission(
    submission_id: int,
    submission_data: SubmissionUpdate,
    db: AsyncSession = Depends(get_db),
    current_admin: Admin = Depends(get_current_active_admin)
):
    """更新提交状态"""
    result = await db.execute(
        select(Submission)
        .options(selectinload(Submission.answers))
        .where(Submission.id == submission_id)
    )
    submission = result.scalar_one_or_none()
    if not submission:
        raise HTTPException(status_code=404, detail="提交记录不存在")
    
    update_data = submission_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(submission, key, value)
    
    # 如果状态发生变化，记录处理信息
    if "status" in update_data and update_data["status"] != SubmissionStatus.PENDING:
        submission.admin_id = current_admin.id
        submission.processed_at = datetime.utcnow()
    
    await db.commit()
    await db.refresh(submission)
    return submission


@router.post("/{submission_id}/approve")
async def approve_submission(
    submission_id: int,
    note: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_admin: Admin = Depends(get_current_active_admin)
):
    """批准提交"""
    result = await db.execute(
        select(Submission).where(Submission.id == submission_id)
    )
    submission = result.scalar_one_or_none()
    if not submission:
        raise HTTPException(status_code=404, detail="提交记录不存在")
    
    submission.status = SubmissionStatus.APPROVED
    submission.admin_id = current_admin.id
    submission.admin_note = note
    submission.processed_at = datetime.utcnow()
    
    await db.commit()
    return {"message": "已批准"}


@router.post("/{submission_id}/reject")
async def reject_submission(
    submission_id: int,
    note: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_admin: Admin = Depends(get_current_active_admin)
):
    """拒绝提交"""
    result = await db.execute(
        select(Submission).where(Submission.id == submission_id)
    )
    submission = result.scalar_one_or_none()
    if not submission:
        raise HTTPException(status_code=404, detail="提交记录不存在")
    
    submission.status = SubmissionStatus.REJECTED
    submission.admin_id = current_admin.id
    submission.admin_note = note
    submission.processed_at = datetime.utcnow()
    
    await db.commit()
    return {"message": "已拒绝"}
