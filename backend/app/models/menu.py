"""
菜单相关数据模型
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.sql import func
from ..database import Base


class Menu(Base):
    """自定义菜单按钮模型"""
    __tablename__ = "menus"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, comment="按钮名称")
    icon = Column(String(50), nullable=True, comment="按钮图标(emoji)")
    order = Column(Integer, default=0, comment="排序序号")
    flow_id = Column(Integer, nullable=True, comment="关联的流程ID")
    is_active = Column(Boolean, default=True, comment="是否激活")
    buttons_per_row = Column(Integer, default=2, comment="每行按钮数")
    description = Column(Text, nullable=True, comment="描述")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), comment="更新时间")
    
    def __repr__(self):
        return f"<Menu {self.name}>"
