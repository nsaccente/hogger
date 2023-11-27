from abc import ABCMeta, abstractmethod, abstractstaticmethod
from inspect import cleandoc
from typing import Optional

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
    id: int = Field(
        default=-1,
        description=cleandoc(
            """
            The primary identifier for the entity in it's respective table.
            This is effectively the db_key in the Hoggerstate table.
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
    def hogger_identifier(self) -> str:
        pass

    @abstractmethod
    def update_id(
        self,
        cursor: Cursor,
        new_id: Optional[int] = None,
        next_id_iterfunc: Optional[callable] = None,
    ) -> None:
        pass

    @abstractmethod
    def diff(self, other: "Entity") -> ("Entity", dict[str, any]):
        pass

    @abstractmethod
    def delete(self, cursor: Cursor) -> str:
        pass

    @abstractmethod
    def insert(self, cursor: Cursor) -> str:
        pass
