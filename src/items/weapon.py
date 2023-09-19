import abc
from pydantic import BaseModel, Field
from typing import Literal, Union
from typing_extensions import Annotated

from .item import Item
from src.misc import Money


class Weapon(Item, abc.ABC):
    item_class: int = 2


class OneHandedAxe(Weapon):
    type: Literal['OneHandedAxe']
    item_subclass: int = 0
    

class TwoHandedAxe(Weapon):
    type: Literal['TwoHandedAxe']
    item_subclass:int = 1


class Bow(Weapon):
    type: Literal['Bow']
    item_subclass: int = 2


class Gun(Weapon):
    type: Literal['Gun']
    item_subclass: int = 3


class OneHandedMace(Weapon):
    type: Literal['OneHandedMace']
    item_subclass: int = 4


class TwoHandedMace(Weapon):
    type: Literal['TwoHandedMace']
    item_subclass: int = 5


class Polearm(Weapon):
    type: Literal['Polearm']
    item_subclass: int = 6


class OneHandedSword(Weapon):
    type: Literal['OneHandedSword']
    item_subclass: int = 7

class TwoHandedSword(Weapon):
    type: Literal['TwoHandedSword']
    item_subclass: int = 8


# 8 is obsolete


class Staff(Weapon):
    type: Literal['Staff']
    item_subclass: int = 10


# 11 & 12 are "Exotic"

class FistWeapon(Weapon):
    type: Literal['FistWeapon']
    item_subclass: int = 13


class Misc(Weapon):
    """Blacksmith Hammer, Mining Pick, etc."""
    type: Literal['Misc']
    item_subclass: int = 14


class Dagger(Weapon):
    type: Literal['Dagger']
    item_subclass: int = 15


class Thrown(Weapon):
    type: Literal['Thrown']
    item_subclass: int = 16


class Spear(Weapon):
    type: Literal['Spear']
    item_subclass: int = 17


class Crossbow(Weapon):
    type: Literal['Crossbow']
    item_subclass: int = 18


class Wand(Weapon):
    type: Literal['Wand']
    item_subclass: int = 19


class FishingPole(Weapon):
    type: Literal['FishingPole']
    item_subclass: int = 20