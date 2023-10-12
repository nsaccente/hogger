from inspect import cleandoc
from typing import Any

from pydantic import BaseModel, Field, model_validator

from hogger.util import LookupID


class ItemSockets(BaseModel):
    socketBonus: LookupID = Field(
        default=0, 
        serialization_alias="socketBonus",
        ge=0
    )
    properties: LookupID = Field(
        default=0, 
        serialization_alias="GemProperties",
        ge=0,
    )
    meta: int = Field(
        default=0,
        description=cleandoc(
            """
            The number of meta sockets. Default is 0.
            """
        ),
        ge=0,
    )
    red: int = Field(
        default=0,
        description=cleandoc(
            """
            The number of red sockets. Default is 0.
            """
        ),
        ge=0,
    )
    yellow: int = Field(
        default=0,
        description=(
            """
            The number of yellow sockets. Default is 0.
            """
        ),
        ge=0,
    )
    blue: int = Field(
        default=0,
        description=cleandoc(
            """
            The number of blue sockets. Default is 0.
            """
        ),
        ge=0,
    )

    # TODO
    @model_validator(mode="after")
    def ensure_3_of_4_socket_colors(cls, data: Any) -> Any:
        return data

    # @staticmethod
    # def from_sql(
    #     sql_data: dict[str, any],
    #     sql_to_model: dict[str, str]={
    #     },
    # ) -> "ItemSockets":
    #     params = {}
    #     for sql_field, model_field in sql_to_model.items():
    #         params[model_field] = sql_data[sql_field] 
    #     return Requires(*params)