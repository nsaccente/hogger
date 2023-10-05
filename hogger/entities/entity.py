from abc import ABCMeta
from inspect import cleandoc
from typing import Any

from pydantic import BaseModel, Field


class Entity(
    BaseModel,
    metaclass=ABCMeta,
):
    type: Any = Field(
        description=cleandoc(
            """
            This field tells the parser which object to use.
            """
        ),
    )

    def to_sql(self):
        dump = self.model_dump()
        for k, v in dump.items():
            print(k, v)
        return ""
