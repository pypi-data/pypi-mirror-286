from typing import Type
from sqlalchemy.orm import Session, declarative_base, Query
from .constants import _T
from .middleware import ctx

_Base = declarative_base()


class DeclarativeModel(_Base):
    """基础模型类，提供了查询和会话的封装"""
    __abstract__ = True

    @classmethod
    def query(cls: Type[_T], *columns):
        query = cls.session().query(*columns if columns else (cls,))  # type: Query[Type[_T]]
        return query

    @classmethod
    def session(cls) -> Session:
        return ctx.session