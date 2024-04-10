from asyncio import current_task
from collections.abc import AsyncGenerator

from sqlalchemy import URL
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_scoped_session,
    async_sessionmaker,
    create_async_engine,
)

from configs.settings import settings
from dependencies.context.session import close_session


def create_engine_and_session(url: str | URL):
    try:
        # Create SQLAlchemy engine
        engine = create_async_engine(
            url,
            # application_name is set to help to identify the sessions
            connect_args={"server_settings": {"application_name": settings.DB_APPNAME}},
            # ensure that the connection is ready to be used
            pool_pre_ping=True,
            # number of connections that will be kept persistently in the pool
            #
            # Note that the pool begins with no connections
            # once this number of connections is requested, that number of connections will remain
            #
            # pool_size can be set to 0 to indicate no size limit
            pool_size=20,
            # The maximum overflow size of the pool.
            # When the number of checked-out connections reaches the size set in pool_size,
            # additional connections will be returned up to this limit.
            #  When those additional connections are returned to the pool, they are disconnected and discarded.
            max_overflow=5,
            # False to disable SQL query logging
            echo=settings.ECHO_SQL,
        )
    except Exception as e:
        print(e)
    else:
        # async_sessionmaker: a factory for new AsyncSession objects
        db_session = async_sessionmaker(
            bind=engine, autoflush=False, expire_on_commit=False
        )
        return engine, db_session


engine, async_session_factory = create_engine_and_session(settings.SQLALCHEMY_DATABASE_URL)  # type: ignore

SessionLocal = async_scoped_session(async_session_factory, scopefunc=current_task)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as db:
        try:
            yield db
        finally:
            await close_session(db)
