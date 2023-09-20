from pydantic import BaseModel, Field, FieldValidationInfo, field_validator
import abc
from typing import Optional
from src.misc import Money
from enum import Enum


class ItemQuality(Enum):
    Poor = 0
    Common = 1
    Uncommon = 2
    Rare = 3
    Epic = 4
    Legendary = 5
    Artifact = 6
    BoA = 7


class ItemClass(Enum):
    Consumable = 0
    Container = 1
    Weapon = 2
    Gem = 3
    Armor = 4
    Reagent = 5
    Projectile = 6
    TradeGoods = 7
    Generic_OBSELETE = 8
    Money_OBSELETE = 9
    Quiver = 11
    Quest = 12
    Key = 13
    Permanent_OBSELETE = 14
    Misc = 15
    Glyph = 16


class ItemInventoryType(Enum):
    NoEquip = 0
    Head = 1
    Neck = 2
    Shoulders = 3
    Body = 4
    Chest = 5
    Waist = 6
    Legs = 7
    Feet = 8
    Wrists = 9
    Hands = 10
    Finger = 11
    Trinket = 12
    WeaponOneHanded = 13
    Shield = 14
    Ranged = 15
    Cloak = 16
    WeaponTwoHanded = 17
    Bag = 18
    Tabard = 19
    Robe = 20
    MainHand = 21
    OffHand = 22
    Holdable = 23
    Ammo = 24
    Thrown = 25
    RangedRight = 26
    Quiver = 27
    Relic = 28


class ItemMaterial(Enum):
    Consumables = -1
    Undefined = 0
    Metal = 1
    Wood = 2
    Liquid = 3
    Jewelry = 4
    Chain = 5
    Plate = 6
    Cloth = 7
    Leather = 8


class ItemBinding(Enum):
    Never = 0
    OnPickup = 1
    OnEquip = 2
    OnUse = 3
    QuestItem = 4
    QuestItem1 = 5
    

class FoodType(Enum):
    Meat = 1
    Fish = 2
    Cheese = 3
    Bread = 4
    Fungus = 5
    Fruit = 6
    RawMeat = 7
    RawFish = 8


class TotemCategory(Enum):
    SkinningKnife_OLD = 1
    EarthTotem = 2
    AirTotem = 3
    FireTotem = 4
    WaterTotem = 5
    RunedCopperRod = 6
    RunedSilverRod = 7
    RunedGoldenod = 8
    RunedTruesilverRod = 9
    RunedArcaniteRod = 10
    MiningPick_OLD = 11
    PhilosophersStone = 12
    BlacksmithHammer_OLD = 13
    ArclightSpanner = 14
    GyromaticMicroAdjustor = 15
    MasterTotem = 21
    RunedFelIronRod = 41
    RunedAdamantiteRod = 62
    RunedEterniumRod = 63
    HollowQuill = 81
    RunedAzuriteRod = 101
    VirtuosoInkingSet = 121
    Drums = 141
    GnomishArmyKnife = 161
    BlacksmithHammer = 162
    MiningPick = 165
    SkinningKnife = 166
    HammerPick = 167
    BladedPickaxe = 168
    FlintAndTinder = 169
    RunedCobaltRod = 189
    RunedTitaniumRod = 190

class ItemStat(Enum):
    Mana = 0
    Health = 1
    Agility = 3
    Strength = 4
    Intellect = 5
    Spirit = 6
    Stamina = 7
    DefenseRating = 12
    DodgeRating = 13
    ParryRating = 14
    BlockRating = 15
    MeleeHitRating = 16
    RangedHitRating = 17
    SpellHitRating = 18
    MeleeCritRating = 19
    RangedCritRating = 20
    SpellCritRating = 21
    MeleeAvoidanceRating = 22
    RangedAvoidanceRating = 23
    SpellAvoidanceRating = 24
    MeleeCritAvoidanceRating = 25
    RangedCritAvoidanceRating = 26
    SpellCritAvoidanceRating = 27
    MeleeHasteRating = 28
    RangedHasteRating = 29
    SpellHasteRating = 30
    HitRating = 31
    CritRating = 32
    HitAvoidanceRating = 33
    CritAvoidanceRating = 34
    ResilienceRating = 35
    HasteRating = 36
    ExpertiseRating = 37
    AttackPower = 38
    RangedAttackPower = 39
    FeralAttackPower_OLD = 40
    SpellHealing = 41
    SpellDamage = 42
    ManaRegen = 43
    ArmorPenetration = 44
    SpellPower = 45
    HealthRegen = 46
    SpellPenetration = 47
    Block = 48


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