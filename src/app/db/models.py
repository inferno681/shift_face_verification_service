from datetime import datetime
from typing import Annotated

from sqlalchemy import Float, ForeignKey, String, text
from sqlalchemy.dialects.postgresql import ARRAY, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import sync_engine
from app.db.basemodels import Base

intpk = Annotated[int, mapped_column(primary_key=True)]
intfk_user = Annotated[
    int,
    mapped_column(ForeignKey('user.id', ondelete='CASCADE')),
]


Base.metadata.reflect(sync_engine, only=['user'])


class User(Base):
    """Модель пользователя."""

    __table__ = Base.metadata.tables['user']
    embedding: Mapped['Embedding'] = relationship(back_populates='user')


class Embedding(Base):
    """Модель Транзакции."""

    id: Mapped[intpk]
    user_id: Mapped[int] = mapped_column(
        ForeignKey('user.id', ondelete='CASCADE'),
    )
    link: Mapped[str] = mapped_column(String(150))
    embedding: Mapped[ARRAY] = mapped_column(ARRAY(Float))
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=text("TIMEZONE('utc', now())"),
    )
    user: Mapped['User'] = relationship('User', back_populates='embedding')
