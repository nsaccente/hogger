from inspect import cleandoc
from typing import Any

from pydantic import BaseModel, Field, model_validator
from mysql.connector.cursor_cext import CMySQLCursor as Cursor

from hogger.types import LookupID


class ItemSockets(BaseModel):
    socketBonus: LookupID = Field(
        default=0, 
        serialization_alias="socketBonus",
    )
    properties: LookupID = Field(
        default=0, 
        serialization_alias="GemProperties",
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

    @staticmethod
    def from_sql(
        GemProperties="GemProperties",
        socketBonus="socketBonus",
        socketColor_1="socketColor_1",
        socketColor_2="socketColor_2",
        socketColor_3="socketColor_3",
        socketContent_1="socketContent_1",
        socketContent_2="socketContent_2",
        socketContent_3="socketContent_3",
    ):
        def from_sql(
            sql_dict: dict[str, any], 
            cursor: Cursor,
            field_type: type,
        ) -> ItemSockets:
            args = {1: 0, 2: 0, 4: 0, 8: 0}
            if socketColor_1 in args: 
                args[socketColor_1] += socketContent_1
            if socketColor_2 in args: 
                args[socketColor_2] += socketContent_2
            if socketColor_3 in args: 
                args[socketColor_3] += socketContent_3
            args["meta"] = args.pop(1)
            args["red"] = args.pop(2)
            args["yellow"] = args.pop(4)
            args["blue"] = args.pop(8)
            return ItemSockets(
                socketBonus=sql_dict[socketBonus],
                properties=sql_dict[GemProperties],
                **args,
            )
        return from_sql