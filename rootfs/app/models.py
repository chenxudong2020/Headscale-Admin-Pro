from sqlalchemy import DateTime, ForeignKey, Index, Integer, LargeBinary, Numeric, String, Text, text # type: ignore
from typing import List, Optional
from flask_login import UserMixin
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship # type: ignore
import datetime
import decimal

class Base(DeclarativeBase):
    pass



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


class ApiKeys(Base):
    __tablename__ = 'api_keys'
    __table_args__ = (
        Index('idx_api_keys_prefix', 'prefix', unique=True),
    )

    id: Mapped[Optional[int]] = mapped_column(Integer, primary_key=True)
    prefix: Mapped[Optional[str]] = mapped_column(Text)
    hash: Mapped[Optional[bytes]] = mapped_column(LargeBinary)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    expiration: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    last_seen: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)


class Migrations(Base):
    __tablename__ = 'migrations'

    id: Mapped[Optional[str]] = mapped_column(Text, primary_key=True)


class Policies(Base):
    __tablename__ = 'policies'
    __table_args__ = (
        Index('idx_policies_deleted_at', 'deleted_at'),
    )

    id: Mapped[Optional[int]] = mapped_column(Integer, primary_key=True)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    deleted_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    data: Mapped[Optional[str]] = mapped_column(Text)
    user_id: Mapped[Optional[int]] = mapped_column(Integer)




class Users(Base,UserMixin):
    __tablename__ = 'users'
    __table_args__ = (
        Index('idx_name_no_provider_identifier', 'name', unique=True),
        Index('idx_name_provider_identifier', 'name', 'provider_identifier', unique=True),
        Index('idx_provider_identifier', 'provider_identifier', unique=True),
        Index('idx_users_deleted_at', 'deleted_at')
    )

    id: Mapped[Optional[int]] = mapped_column(Integer, primary_key=True)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    deleted_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    name: Mapped[Optional[str]] = mapped_column(Text)
    display_name: Mapped[Optional[str]] = mapped_column(Text)
    email: Mapped[Optional[str]] = mapped_column(Text)
    provider_identifier: Mapped[Optional[str]] = mapped_column(Text)
    provider: Mapped[Optional[str]] = mapped_column(Text)
    profile_pic_url: Mapped[Optional[str]] = mapped_column(Text)

    password: Mapped[Optional[str]] = mapped_column(Text)
    expire: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    cellphone: Mapped[Optional[str]] = mapped_column(Text)
    role: Mapped[Optional[str]] = mapped_column(Text)
    enable: Mapped[Optional[str]] = mapped_column(Text)

    pre_auth_keys: Mapped[List['PreAuthKeys']] = relationship('PreAuthKeys', back_populates='user')
    nodes: Mapped[List['Nodes']] = relationship('Nodes', back_populates='user')




class PreAuthKeys(Base):
    __tablename__ = 'pre_auth_keys'

    id: Mapped[Optional[int]] = mapped_column(Integer, primary_key=True)
    key: Mapped[Optional[str]] = mapped_column(Text)
    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey('users.id'))
    reusable: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric)
    ephemeral: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric, server_default=text('false'))
    used: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric, server_default=text('false'))
    tags: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    expiration: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)

    user: Mapped[Optional['Users']] = relationship('Users', back_populates='pre_auth_keys')
    nodes: Mapped[List['Nodes']] = relationship('Nodes', back_populates='auth_key')


class Nodes(Base):
    __tablename__ = 'nodes'

    id: Mapped[Optional[int]] = mapped_column(Integer, primary_key=True)
    machine_key: Mapped[Optional[str]] = mapped_column(Text)
    node_key: Mapped[Optional[str]] = mapped_column(Text)
    disco_key: Mapped[Optional[str]] = mapped_column(Text)
    endpoints: Mapped[Optional[str]] = mapped_column(Text)
    host_info: Mapped[Optional[str]] = mapped_column(Text)
    ipv4: Mapped[Optional[str]] = mapped_column(Text)
    ipv6: Mapped[Optional[str]] = mapped_column(Text)
    hostname: Mapped[Optional[str]] = mapped_column(Text)
    given_name: Mapped[Optional[str]] = mapped_column(String(63))
    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey('users.id'))
    register_method: Mapped[Optional[str]] = mapped_column(Text)
    forced_tags: Mapped[Optional[str]] = mapped_column(Text)
    auth_key_id: Mapped[Optional[int]] = mapped_column(ForeignKey('pre_auth_keys.id'))
    expiry: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    approved_routes: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    deleted_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)

    auth_key: Mapped[Optional['PreAuthKeys']] = relationship('PreAuthKeys', back_populates='nodes')
    user: Mapped[Optional['Users']] = relationship('Users', back_populates='nodes')
