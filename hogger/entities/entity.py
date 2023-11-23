from abc import ABCMeta, abstractmethod, abstractstaticmethod
from inspect import cleandoc

from mysql.connector.cursor_cext import CMySQLCursor as Cursor
from pydantic import BaseModel, Field


class Entity(
    BaseModel,
    metaclass=ABCMeta,
):
    type: str = Field(
        description=cleandoc(
            """
            This field tells the parser which object to use
            """,
        ),
    )

    @abstractstaticmethod
    def from_hoggerstate(
        db_key: int,
        hogger_id: str,
        cursor: Cursor,
    ) -> "Entity":
        pass

    @abstractmethod
    def get_db_key(self) -> int:
        pass

    @abstractmethod
    def set_db_key(self) -> None:
        pass

    @abstractmethod
    def hogger_identifier(self) -> str:
        pass

    @abstractmethod
    def diff(self, other: "Entity") -> ("Entity", dict[str, any]):
        pass

    @abstractmethod
    def apply(self, cursor: Cursor) -> None:
        pass
