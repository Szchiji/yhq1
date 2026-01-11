"""
钱包和交易记录数据模型
"""
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Enum as SQLEnum, Numeric
from sqlalchemy.sql import func
from decimal import Decimal
import enum
from ..database import Base


class TransactionType(str, enum.Enum):
    """交易类型枚举"""
    DEPOSIT = "deposit"  # 充值
    WITHDRAW = "withdraw"  # 提现
    REWARD = "reward"  # 奖励
    DEDUCT = "deduct"  # 扣除
    REFUND = "refund"  # 退款


class TransactionStatus(str, enum.Enum):
    """交易状态枚举"""
    PENDING = "pending"  # 待处理
    COMPLETED = "completed"  # 已完成
    FAILED = "failed"  # 失败
    CANCELLED = "cancelled"  # 已取消


class Wallet(Base):
    """用户钱包模型"""
    __tablename__ = "wallets"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False, comment="用户ID")
    balance = Column(Numeric(10, 2), default=Decimal("0.00"), comment="余额")
    points = Column(Integer, default=0, comment="积分")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), comment="更新时间")
    
    def __repr__(self):
        return f"<Wallet user_id={self.user_id} balance={self.balance}>"


class Transaction(Base):
    """交易记录模型"""
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    wallet_id = Column(Integer, ForeignKey("wallets.id", ondelete="CASCADE"), nullable=False, comment="钱包ID")
    transaction_type = Column(SQLEnum(TransactionType), nullable=False, comment="交易类型")
    amount = Column(Numeric(10, 2), nullable=False, comment="金额")
    points = Column(Integer, default=0, comment="积分变化")
    status = Column(SQLEnum(TransactionStatus), default=TransactionStatus.PENDING, comment="交易状态")
    description = Column(Text, nullable=True, comment="描述")
    reference_id = Column(String(255), nullable=True, comment="关联ID")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), comment="更新时间")
    
    def __repr__(self):
        return f"<Transaction {self.id} {self.transaction_type}>"
