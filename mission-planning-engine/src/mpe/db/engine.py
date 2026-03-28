"""Database engine and session management."""

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from mpe.db.models import Base

DEFAULT_DB_URL = "postgresql+asyncpg://mpe:mpe@localhost:5432/mpe_c2"


class Database:
    """Manages the database connection lifecycle."""

    def __init__(self, url: str = DEFAULT_DB_URL) -> None:
        self._url = url
        self._engine = None
        self._session_factory = None

    async def connect(self) -> None:
        """Create the async engine and session factory."""
        self._engine = create_async_engine(
            self._url, echo=False, pool_size=10,
        )
        self._session_factory = async_sessionmaker(
            self._engine, class_=AsyncSession, expire_on_commit=False,
        )

    async def disconnect(self) -> None:
        """Dispose of the engine and release all connections."""
        if self._engine:
            await self._engine.dispose()

    async def create_tables(self) -> None:
        """Create all tables defined in the ORM models."""
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    def session(self) -> AsyncSession:
        """Return a new async session from the factory."""
        return self._session_factory()
