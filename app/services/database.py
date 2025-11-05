from __future__ import annotations

from contextlib import contextmanager
from typing import Iterator

from sqlalchemy.orm import Session, sessionmaker

from models.tust_models import Base, create_sqlite_engine


def get_engine(db_url: str | None = None, echo: bool = False):
    url = db_url or "sqlite:///tust.db"
    return create_sqlite_engine(url, echo=echo)


def get_session_factory(db_url: str | None = None, echo: bool = False):
    engine = get_engine(db_url, echo=echo)
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)


@contextmanager
def db_session(db_url: str | None = None, echo: bool = False) -> Iterator[Session]:
    factory = get_session_factory(db_url, echo=echo)
    session = factory()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
