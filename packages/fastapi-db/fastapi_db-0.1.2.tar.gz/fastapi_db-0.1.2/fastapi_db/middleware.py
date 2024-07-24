# -*- coding:utf-8 -*-
from contextvars import ContextVar
from typing import Optional, Union
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker, Session
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp
from .exceptions import SessionInitError, SessionContextError
from .transaction_enums import Propagation, Isolation

_middleware: Optional['FastAPIDBMiddleware'] = None
_session_context: ContextVar[Session] = ContextVar('fastapi_db')
_SESSION_MISSING_MESSAGE = '未找到上下文Session对象，请检查是否正确添加中间件，如非API获取Session请手动或在函数添加装饰器'


class FastAPIDBMiddleware(BaseHTTPMiddleware):

    engine: Optional[Engine] = None
    session_factory: Optional[sessionmaker] = None

    def __init__(
        self,
        app: ASGIApp,
        datasource_url: Optional[Union[str, URL]] = None,
        engine: Optional[Engine] = None,
        engine_kwargs: dict = None,
        session_kwargs: dict = None,
        autocommit: bool = True
    ):
        super().__init__(app)
        self.autocommit = autocommit
        self.engine_kwargs = engine_kwargs or {}
        self.session_kwargs = session_kwargs or {}

        if not datasource_url and not engine:
            raise ValueError('您需要传递一个datasource_url或一个引擎参数。')

        if not engine:
            self.engine = create_engine(datasource_url, **self.engine_kwargs)
        else:
            self.engine = engine

        self.session_factory = sessionmaker(bind=self.engine, **self.session_kwargs)
        global _middleware
        _middleware = self

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        with db(autocommit=self.autocommit):
            response = await call_next(request)
        return response


def _check_init():
    if _middleware is None:
        raise SessionInitError(f'请先添加 `{FastAPIDBMiddleware.__name__}` 中间件')


class TransactionContext(object):
    """事务上下文"""

    @property
    def session(self) -> Session:
        _check_init()
        session = _session_context.get()
        if session is None:
            raise SessionContextError(_SESSION_MISSING_MESSAGE)
        return session


class DBSession(TransactionContext):
    """DBSession"""

    def __init__(
        self,
        propagation: Propagation = Propagation.REQUIRED,
        isolation: Isolation = Isolation.DEFAULT,
        autocommit: bool = None
    ):
        self._token = None
        self.middleware: Optional[FastAPIDBMiddleware] = None
        self.propagation = propagation
        self.isolation = isolation
        self.autocommit = autocommit

    def __enter__(self):
        _check_init()
        self.middleware = _middleware
        self.autocommit = self.middleware.autocommit
        self._token = _session_context.set(self.middleware.session_factory())
        return type(self)

    def __exit__(self, exc_type, exc_value, traceback):
        sess = _session_context.get()
        if exc_type is not None:
            sess.rollback()

        if self.autocommit:
            sess.commit()

        sess.close()
        _session_context.reset(self._token)


ctx = TransactionContext()
db = DBSession