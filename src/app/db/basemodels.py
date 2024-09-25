from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, declared_attr


class Base(AsyncAttrs, DeclarativeBase):
    """Abstract base class for tables creation."""

    __abstract__ = True

    @declared_attr
    def __tablename__(cls):
        """Table name from class name."""
        return cls.__name__.lower()
