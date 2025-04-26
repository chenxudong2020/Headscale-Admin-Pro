from sqlalchemy import DateTime, ForeignKey, Index, Integer, LargeBinary, Numeric, String, Text, text # type: ignore
from sqlalchemy.orm import relationship, Mapped, mapped_column # type: ignore
import datetime
from models import Users as OriginalUsers, Base,ApiKeys as OriginalApiKeys
from models import Policies as OriginalPolicies, PreAuthKeys as OriginalPreAuthKeys, Nodes as OriginalNodes
from typing import List, Optional

# 新增系统配置表
class Configs(Base):
    __tablename__ = 'configs'
    id: Mapped[Optional[int]] = mapped_column(Integer, primary_key=True,autoincrement=True)
    acceptreg: Mapped[Optional[str]] = mapped_column(Text)
    acceptlogin: Mapped[Optional[str]] = mapped_column(Text)
    acceptnewlogin: Mapped[Optional[str]] = mapped_column(Text)

# 新增系统日志表
class Logs(Base):
    __tablename__ = 'logs'
    id: Mapped[Optional[int]] = mapped_column(Integer, primary_key=True,autoincrement=True)
    user_id: Mapped[Optional[int]] = mapped_column(Integer)
    content: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)

# 扩展用户模型
class Users(OriginalUsers):
        __tablename__ = 'users'
        __table_args__ = {'extend_existing': True}
        password: Mapped[Optional[str]] = mapped_column(Text)
        expire: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
        cellphone: Mapped[Optional[str]] = mapped_column(Text)
        role: Mapped[Optional[str]] = mapped_column(Text)
        enable: Mapped[Optional[str]] = mapped_column(Text)

class ApiKeys(OriginalApiKeys):
        __tablename__ = 'api_keys'
        __table_args__ = {'extend_existing': True}

#扩展ACL模型
class Policies(OriginalPolicies):
        __tablename__ = 'policies'
        __table_args__ = {'extend_existing': True}
        user_id: Mapped[Optional[int]] = mapped_column(Integer)

class PreAuthKeys(OriginalPreAuthKeys):
        __tablename__ = 'pre_auth_keys'
        __table_args__ = {'extend_existing': True}

class Nodes(OriginalNodes):
        __tablename__ = 'nodes'
        __table_args__ = {'extend_existing': True}      

