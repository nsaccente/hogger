from enum import IntEnum
from inspect import cleandoc

from mysql.connector.cursor_cext import CMySQLCursor as Cursor
from pydantic import (
    BaseModel,
    Field,
    FieldValidationInfo,
    SerializationInfo,
    field_serializer,
    field_validator,
)

from hogger.types import EnumUtils


class DamageType(IntEnum):
    Normal = 0
    Holy = 1
    Fire = 2
    Nature = 3
    Frost = 4
    Shadow = 5
    Arcane = 6


class Damage(BaseModel):
    min1: int = Field(
        default=0,
        description=cleandoc(
            """
            The minimum, primary damage of the item.
            """,
        ),
        serialization_alias="dmg_min1",
        ge=0,
    )
    max1: int = Field(
        default=0,
        description=cleandoc(
            """
            The maximum, primary damage of the item.
            """,
        ),
        serialization_alias="dmg_max1",
        ge=0,
    )
    type1: DamageType = Field(
        default=DamageType.Normal,
        description=cleandoc(
            """
            The type of primary damage inflicted.
            """,
        ),
        serialization_alias="dmg_type1",
    )
    min2: int = Field(
        default=0,
        description=cleandoc(
            """
            The minimum, secondary damage of the item.
            """,
        ),
        serialization_alias="dmg_min2",
        ge=0,
    )
    max2: int = Field(
        default=0,
        description=cleandoc(
            """
            The maximum, secondary damage of the item.
            """,
        ),
        serialization_alias="dmg_max2",
        ge=0,
    )
    type2: DamageType = Field(
        default=DamageType.Normal,
        description=cleandoc(
            """
            The type of secondary damage inflicted.
            """,
        ),
        serialization_alias="dmg_type2",
    )


    @field_validator(
        "type1",
        "type2",
        mode="before",
    )
    def parse_damage_type(
        cls,
        v: (str | int),
        info: FieldValidationInfo,
    ) -> DamageType | int:
        vals = [i.value for i in DamageType]
        if isinstance(v, int):
            if v in vals:
                return DamageType(v)
            else:
                return v
        elif isinstance(v, str):
            return DamageType[v]
        elif isinstance(v, DamageType):
            return v
        else:
            raise Exception(f'"{v}" is not a valid damage type')


    @field_serializer(
        "type1",
        "type2",
        when_used="json-unless-none",
    )
    def serialize_damage_Type(
        self,
        v: (DamageType | int),
        info: SerializationInfo,
    ) -> str | int:
        if isinstance(v, DamageType):
            return v.name
        return v


    @staticmethod
    def from_sql(
        min1: str = "dmg_min1",
        max1: str = "dmg_max1",
        type1: str = "dmg_type1",
        min2: str = "dmg_min2",
        max2: str = "dmg_max2",
        type2: str = "dmg_type2",
    ):
        def from_sql(
            sql_dict: dict[str, any],
            cursor: Cursor = None,
            field_type: type = None,
        ) -> Damage:
            return Damage(
                min1=sql_dict[min1],
                max1=sql_dict[max1],
                type1=EnumUtils.resolve(sql_dict[type1], DamageType),
                min2=sql_dict[min2],
                max2=sql_dict[max2],
                type2=EnumUtils.resolve(sql_dict[type2], DamageType),
            )
        return from_sql


    @staticmethod
    def to_sql(
        model_field: str,
        min1: str = "dmg_min1",
        max1: str = "dmg_max1",
        type1: str = "dmg_type1",
        min2: str = "dmg_min2",
        max2: str = "dmg_max2",
        type2: str = "dmg_type2",
    ):
        def to_sql(
            model_field: str,
            model_dict: dict[str, any],
            cursor: Cursor,
            field_type: type,
        ) -> dict[str, any]:
            d: "Damage" = model_dict[model_field]
            return {
                min1: int(d.min1),
                max1: int(d.max1),
                type1: int(d.type1),
                min2: int(d.min2),
                max2: int(d.max2),
                type2: int(d.type2),
            }
        return to_sql