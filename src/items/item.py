from pydantic import BaseModel, Field, FieldValidationInfo, field_validator
import abc
from typing import Optional
from src.misc import Money

ITEM_QUALITIES = {
    "Poor": 0,
    "Common": 1,
    "Uncommon": 2,
    "Rare": 3,
    "Epic": 4,
    "Legendary": 5,
    "Artifact": 6,
    "BoA": 7,
}

class Item(BaseModel, abc.ABC):
    name: str = Field(
        description="The name of the item",
    )
    description: Optional[str] = Field(
        default=None,
        description=(
            "The description that appears in yellow letters at the bottom of "
            "the item tooltip"
        ),
    )
    scriptName: Optional[str] = Field(
        default=None, 
        serialization_alias="ScriptName",
        description="The name of the script that the item should use",
    )
    soundOverride: int = Field(
        default=-1, 
        serialization_alias="SoundOverride",
        description=(
            "Each weapon type plays a unique sound on impact, which can be "
            "overriden by the unique sound of a different weapon type"
        ),
    )
    displayID: int = Field(
        serialization_alias="displayid",
        description="Controls both the model appearance and icon.",
    )
    quality: str = Field(
        default="Common",
        serialization_alias="Quality",
        description=(
            "The quality of the item; valid values are: Poor, Uncommon, "
            "Common, Rare, Epic, Legendary, Artifact, BoA"
        ),
    )
    buyCount: int = Field(
        default=1,
        serialization_alias="BuyCount",
        description="",
    )
    buyPrice: Money = Field(
        default=Money(gold=0, silver=0, copper=0),
        serialization_alias="BuyPrice",
        description="The cost to purchase this item form a vendor",
    )
    sellPrice: Money = Field(
        default=Money(gold=0, silver=0, copper=0),
        serialization_alias="SellPrice",
        description="The amount a vendor will purchase this item from you for",
    )
    

    @field_validator("quality")
    def check_alphanumeric(cls, v: str, info: FieldValidationInfo) -> str:
        assert v in ITEM_QUALITIES, (
            "\"{}\" is not a valid quality; use one of Poor, Common, "
            "Uncommon, Rare, Epic, Legendary, Artifact, or BoA".format(v)
        )
        return v