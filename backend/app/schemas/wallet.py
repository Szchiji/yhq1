"""
钱包相关 Pydantic Schemas
"""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from decimal import Decimal
from ..models.wallet import TransactionType, TransactionStatus


class WalletSchema(BaseModel):
    """钱包 Schema"""
    id: int
    user_id: int
    balance: Decimal
    points: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class TransactionSchema(BaseModel):
    """交易记录 Schema"""
    id: int
    wallet_id: int
    transaction_type: TransactionType
    amount: Decimal
    points: int
    status: TransactionStatus
    description: Optional[str] = None
    reference_id: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
