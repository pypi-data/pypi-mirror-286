from contextlib import contextmanager
from typing import (
    Optional,
    Type,
    List,
)

from sqlalchemy import Engine, NullPool
from sqlmodel import create_engine, Session as SQLModelSession

from pjdev_sqlmodel.db_models import ModelBase
from pjdev_sqlmodel.settings import SqlModelSettings


class DBContext:
    initialized: bool = False
    engine: Optional[Engine] = None


__ctx = DBContext()


def initialize_engine(
    settings: SqlModelSettings,
    tables: List[Type[ModelBase]],
    echo: bool = False,
) -> Engine:
    if len(tables) == 0:
        raise ValueError("Must specify at least one table")

    database_url = f"sqlite:///{settings.data_path}/{settings.sqlite_filename}"

    engine = create_engine(database_url, echo=echo, poolclass=NullPool)

    for t in tables:
        t.__table__.create(bind=engine, checkfirst=True)

    return engine


def configure_single_context(settings: SqlModelSettings, tables: List[Type[ModelBase]]):
    __ctx.engine = initialize_engine(settings, tables)


@contextmanager
def session_context() -> SQLModelSession:
    with SQLModelSession(__ctx.engine) as session:
        try:
            yield session
        finally:
            session.close()
