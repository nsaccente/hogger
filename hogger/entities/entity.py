from pydantic import BaseModel, Field
from typing import Any, Annotated, Union, Literal
from inspect import cleandoc
from abc import ABCMeta


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
    # type: Literal["Entity"]


    def to_sql(self):
        dump = self.model_dump()
        for k, v in dump.items():
            print(k, v)
        return ""
