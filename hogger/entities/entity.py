from abc import ABCMeta, abstractstaticmethod
from inspect import cleandoc
from typing import Any

from pydantic import BaseModel, Field
from mysql.connector.cursor_cext import CMySQLCursor as Cursor


class Entity(
    BaseModel,
    metaclass=ABCMeta,
):
    type: Any = Field(
        description=cleandoc(
            """
            This field tells the parser which object to use
            """
        ),
    )

    @abstractstaticmethod
    def from_hoggerstate(
        cursor: Cursor,
    ) -> "Entity":
        pass