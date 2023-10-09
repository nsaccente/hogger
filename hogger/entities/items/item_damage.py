from enum import Enum
from inspect import cleandoc

from pydantic import (
    BaseModel,
    Field,
    FieldValidationInfo,
    SerializationInfo,
    field_serializer,
    field_validator,
)


class DamageType(Enum):
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
            """
        ),
        serialization_alias="dmg_min1",
        ge=0,
    )
    max1: int = Field(
        default=0,
        description=cleandoc(
            """
            The maximum, primary damage of the item.
            """
        ),
        serialization_alias="dmg_max1",
        ge=0,
    )
    type1: DamageType = Field(
        default=DamageType.Normal,
        description=cleandoc(
            """
            The type of primary damage inflicted.
            """
        ),
        serialization_alias="dmg_type1",
    )
    min2: int = Field(
        default=0,
        description=cleandoc(
            """
            The minimum, secondary damage of the item.
            """
        ),
        serialization_alias="dmg_min2",
        ge=0,
    )
    max2: int = Field(
        default=0,
        description=cleandoc(
            """
            The maximum, secondary damage of the item.
            """
        ),
        serialization_alias="dmg_max2",
        ge=0,
    )
    type2: DamageType = Field(
        default=DamageType.Normal,
        description=cleandoc(
            """
            The type of secondary damage inflicted.
            """
        ),
        serialization_alias="dmg_type2",
    )

    @field_validator(
        "type1",
        "type2",
        mode="before",
    )
    def parse_damage_type(
        cls, v: (str | int), info: FieldValidationInfo
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
