import abc
from typing import Literal

from pydantic import BaseModel, Field

from .item import Item


class Weapon(Item):
    pass


class OneHandedAxe(Weapon):
    type: Literal["OneHandedAxe"]
    # itemSubclass: int = Field(
    #     default=0,
    #     serialization_alias="subclass",
    # )


class TwoHandedAxe(Weapon):
    type: Literal["TwoHandedAxe"]
    # itemSubclass: int = Field(
    #     default=1,
    #     serialization_alias="subclass",
    # )


class Bow(Weapon):
    type: Literal["Bow"]


class Gun(Weapon):
    type: Literal["Gun"]


#     itemSubclass: int = Field(
#         default=3,
#         serialization_alias="subclass",
#     )


class OneHandedMace(Weapon):
    type: Literal["OneHandedMace"]


#     itemSubclass: int = Field(
#         default=4,
#         serialization_alias="subclass",
#     )
#     inventoryType: int = Field(default=17)


class TwoHandedMace(Weapon):
    type: Literal["TwoHandedMace"]


#     itemSubclass: int = Field(
#         default=5,
#         serialization_alias="subclass",
#     )


class Polearm(Weapon):
    type: Literal["Polearm"]


#     itemSubclass: int = Field(
#         default=6,
#         serialization_alias="subclass",
#     )


class OneHandedSword(Weapon):
    type: Literal["OneHandedSword"]


#     itemSubclass: int = Field(
#         default=7,
#         serialization_alias="subclass",
#     )


class TwoHandedSword(Weapon):
    type: Literal["TwoHandedSword"]


#     itemSubclass: int = Field(
#         default=8,
#         serialization_alias="subclass",
#     )


# # 9 is obsolete


class Staff(Weapon):
    type: Literal["Staff"]


#     itemSubclass: int = Field(
#         default=10,
#         serialization_alias="subclass",
#     )


# # 11 & 12 are "Exotic"


class FistWeapon(Weapon):
    type: Literal["FistWeapon"]


#     itemSubclass: int = Field(
#         default=13,
#         serialization_alias="subclass",
#     )


class Tool(Weapon):
    """Blacksmith Hammer, Mining Pick, etc."""

    type: Literal["Tool"]


#     itemSubclass: int = Field(
#         default=14,
#         serialization_alias="subclass",
#     )


class Dagger(Weapon):
    type: Literal["Dagger"]


#     itemSubclass: int = Field(
#         default=15,
#         serialization_alias="subclass",
#     )


class Thrown(Weapon):
    type: Literal["Thrown"]


#     itemSubclass: int = Field(
#         default=16,
#         serialization_alias="subclass",
#     )


class Spear(Weapon):
    type: Literal["Spear"]


#     itemSubclass: int = Field(
#         default=17,
#         serialization_alias="subclass",
#     )


class Crossbow(Weapon):
    type: Literal["Crossbow"]


#     itemSubclass: int = Field(
#         default=18,
#         serialization_alias="subclass",
#     )


class Wand(Weapon):
    type: Literal["Wand"]


#     itemSubclass: int = Field(
#         default=19,
#         serialization_alias="subclass",
#     )


class FishingPole(Weapon):
    type: Literal["FishingPole"]


#     itemSubclass: int = Field(
#         default=20,
#         serialization_alias="subclass",
#     )
