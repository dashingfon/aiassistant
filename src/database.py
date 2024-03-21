import pathlib
from enum import Enum
from typing import Any, TypeVar, Type, Iterable, Optional
from sqlmodel import SQLModel, Session, create_engine, select, Field


class Sender(str, Enum):
    human = "human"
    ai = "ai"


class NameSpace(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    key: str = Field(index=True, unique=True)
    value: str


class MessageHistory(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    sender: Sender
    message: str


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
    default: list | Any = [],
) -> list[DATA] | Any:
    selection = select(data)  # type: ignore
    if order_by:
        selection = selection.order_by(*order_by)
    if query:
        selection = selection.where(*query)
    if limit:
        selection = selection.limit(limit)
    result = session.exec(selection).all()
    return default if not result else result


def delete(session: Session, *data: DATA) -> None:
    for entry in data:
        session.delete(entry)
    session.commit()


if __name__ == "__main__":
    engine = create_engine(SQLITE_URL, connect_args=CONNECT_ARGS, echo=True)

    def set_chat_cutoff(num: int):
        value = str(num)
        with Session(engine) as session:
            var = NameSpace(key="chat-cutoff", value=value)
            create(session, var)

    def set_api_protection(protect: bool):
        value = "true" if protect else "false"
        with Session(engine) as session:
            var = NameSpace(key="api-protection", value=value)
            create(session, var)

    set_chat_cutoff(0)
    set_api_protection(True)
