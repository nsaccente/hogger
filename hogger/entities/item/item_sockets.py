from inspect import cleandoc

from mysql.connector.cursor_cext import CMySQLCursor as Cursor
from pydantic import BaseModel, Field, model_validator

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
            """,
        ),
        ge=0,
    )
    red: int = Field(
        default=0,
        description=cleandoc(
            """
            The number of red sockets. Default is 0.
            """,
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
            """,
        ),
        ge=0,
    )

    # TODO
    @model_validator(mode="after")
    def ensure_3_of_4_socket_colors(cls, data: any) -> any:
        return data

    @staticmethod
    def from_sql(
        GemProperties="GemProperties",
        socketBonus="socketBonus",
        socket_map={
            "socketColor_1": "socketContent_1",
            "socketColor_2": "socketContent_2",
            "socketColor_3": "socketContent_3",
        },
        # socketColor_1="socketColor_1",
        # socketColor_2="socketColor_2",
        # socketColor_3="socketColor_3",
        # socketContent_1="socketContent_1",
        # socketContent_2="socketContent_2",
        # socketContent_3="socketContent_3",
    ):
        def from_sql(
            sql_dict: dict[str, any],
            cursor: Cursor,
            field_type: type,
        ) -> ItemSockets:
            args = {1: 0, 2: 0, 4: 0, 8: 0}
            for socketColor, socketContent in socket_map.items():
                if socketColor in args:
                    args[socketColor] += socketContent
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

    @staticmethod
    def to_sql(
        GemProperties="GemProperties",
        socketBonus="socketBonus",
        socket_map={
            "socketColor_1": "socketContent_1",
            "socketColor_2": "socketContent_2",
            "socketColor_3": "socketContent_3",
        },
    ):
        def to_sql(
            model_field: str,
            model_dict: dict[str, any],
            cursor: Cursor,
            field_type: type,
        ) -> dict[str, any]:
            attrs = {"meta": 1, "red": 2, "yellow": 4, "blue": 8}
            s: "ItemSockets" = model_dict[model_field]
            it = iter(socket_map.items())
            result = dict()
            for attr, bit in attrs.items():
                socketColor, socketContent = next(it, (None, None))
                if socketColor is None or socketContent is None:
                    continue
                num_sockets = s.__getattribute__(attr)
                if num_sockets > 0:
                    result[socketColor] = attr
                    result[socketContent] = num_sockets
            return result

        return to_sql
