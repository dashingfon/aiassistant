import pathlib
from typing import Any, TypeVar, Type, Iterable
from sqlmodel import SQLModel, Session, create_engine, select


class NameSpace(SQLModel, table=True):
    ...


class MessageHistory(SQLModel, table=True):
    ...

DATA = TypeVar("DATA")
PATH = pathlib.PurePath(__file__).parent.parent
SQLITE_URL = f"sqlite:///{PATH.joinpath('data', 'database.db')}"
CONNECT_ARGS = {"check_same_thread": False}

engine = create_engine(SQLITE_URL, connect_args=CONNECT_ARGS)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def create(session: Session, *entries: DATA) -> None:
    for item in entries:
        session.add(item)
    session.commit()


def read(
    session: Session,
    data: Type[DATA],
    query: Iterable[Any] = [],
    order_by: Iterable[Any] = [],
    limit: int = 0,
) -> list[DATA]:
    selection = select(data)  # type: ignore
    if order_by:
        selection = selection.order_by(*order_by)
    if query:
        selection = selection.where(*query)
    if limit:
        selection = selection.limit(limit)
    result = session.exec(selection)
    return result.all()


def delete(session: Session, *data: DATA) -> None:
    for entry in data:
        session.delete(entry)
    session.commit()


if __name__ == "__main__":
    ...