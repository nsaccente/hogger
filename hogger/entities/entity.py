from abc import ABCMeta, abstractstaticmethod, abstractmethod
from inspect import cleandoc
from typing import Any

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
            """
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
    def db_key(self) -> int:
        pass

    @abstractmethod
    def hogger_identifier(self) -> str:
        pass

    @abstractmethod
    def diff(self, other: "Entity") -> "Entity":
        pass