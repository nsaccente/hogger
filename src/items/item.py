import abc
from enum import Enum

from pydantic import BaseModel, Field, FieldValidationInfo, field_validator

from src.misc import Money


class Quality(Enum):
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


class InventoryType(Enum):
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


class Material(Enum):
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
    Undefined = 0
    Meat = 1
    Fish = 2
    Cheese = 3
    Bread = 4
    Fungus = 5
    Fruit = 6
    RawMeat = 7
    RawFish = 8


class TotemCategory(Enum):
    Undefined = 0
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


class BagFamily(BaseModel):
    Arrows: bool = False
    Bullets: bool = False
    SoulShards: bool = False
    Leatherworking: bool = False
    Inscription: bool = False
    Herbs: bool = False
    Enchanting: bool = False
    Engineering: bool = False
    Keys: bool = False
    Gems: bool = False
    Mining: bool = False
    SoulboundEquipment: bool = False
    VanityPets: bool = False
    CurrencyTokens: bool = False
    QuestItems: bool = False

    def __setitem__(self, key, value):
        setattr(self, key, value)

    def __getitem__(self, key):
        return getattr(self, key)

    def __int__(self):
        return (
            (self.Arrows * 1)
            + (self.Bullets * 2)
            + (self.SoulShards * 4)
            + (self.Leatherworking * 8)
            + (self.Inscription * 16)
            + (self.Herbs * 32)
            + (self.Enchanting * 64)
            + (self.Engineering * 128)
            + (self.Keys * 256)
            + (self.Gems * 512)
            + (self.Mining * 1024)
            + (self.SoulboundEquipment * 2048)
            + (self.VanityPets * 4096)
            + (self.CurrencyTokens * 8192)
            + (self.QuestItems * 16384)
        )


class Item(BaseModel, abc.ABC):
    name: str = Field(
        description="The name of the item",
    )
    description: str = Field(
        default="",
        description=(
            "The description that appears in yellow letters at the bottom of "
            "the item tooltip"
        ),
    )
    scriptName: str = Field(
        default="",
        description="The name of the script that the item should use",
    )
    soundOverride: int = Field(
        default=-1,
        description=(
            "Each weapon type plays a unique sound on impact, which can be "
            "overriden by the unique sound of a different weapon type"
        ),
    )
    displayID: int = Field(
        description="Controls both the model appearance and icon.",
    )
    quality: Quality = Field(
        default=Quality.Common,
        description=(
            "The quality of the item; valid values are: Poor, Uncommon, "
            "Common, Rare, Epic, Legendary, Artifact, BoA"
        ),
    )
    buyCount: int = Field(
        default=1,
        description=(
            "The size of the item stack when sold by vendors. If a vendor has "
            "a limited number of this item available, the vendor's inventory "
            "will increase by this number when the vendor list is refreshed "
            "(see npc.vendor.incrtime)."
        ),
    )
    buyPrice: Money = Field(
        default=Money(gold=0, silver=0, copper=0),
        description="The cost to purchase this item form a vendor",
    )
    sellPrice: Money = Field(
        default=Money(gold=0, silver=0, copper=0),
        description="The amount a vendor will purchase this item from you for",
    )
    inventoryType: InventoryType = Field(
        default=InventoryType.NoEquip,
        description="Is the item equippable? A quest item?",
    )
    maxAmount: int = Field(
        default=0,
        description="The maximum amount that a player can have; use 0 for infinite",
    )
    stackSize: int = Field(
        default=1,
        description="The maximum size of a stack of this item.",
    )
    startsQuest: int = Field(
        default=0,
        description=(
            "The ID of the quest that this item will start if right-clicked. "
            "See quest_template.id"
        ),
    )
    material: Material = Field(
        default=Material.Undefined,
        description="Controls the sound played when moving items in your inventory",
    )
    bagFamily: BagFamily = Field(
        default=BagFamily(),
        description="Dictates what kind of bags this item can be placed in.",
    )
    # randomPropertyItem with RandomProperty = 863
    # Item with RandomSuffix = 24585
    # min(RandomProperty, RandomSuffix) must equal 0.
    containerSlots: int = Field(
        default=0,
        description="If this item is a bag, controls the number of slots it will have",
    )
    specialUse: TotemCategory = Field(
        default=TotemCategory.Undefined,
        description=(
            "Some items are required to complete certain tasks, such as a "
            "shaman's totems, "
        ),
    )

    @field_validator("buyCount", "stackSize")
    def integer_greater_than_zero(cls, v: int, info: FieldValidationInfo) -> int:
        if v <= 0:
            raise Exception("Value for {} must be non-negative".format(info.field_name))
        return v

    @field_validator("displayId", "maxAmount")
    def non_negative_integer(cls, v: int, info: FieldValidationInfo) -> int:
        if v < 0:
            raise Exception("Value for {} must be non-negative".format(info.field_name))
        return v

    @field_validator("buyPrice", "sellPrice", mode="after")
    def prevent_negative_money(cls, v: Money, info: FieldValidationInfo) -> Money:
        if (v.gold < 0) or (v.silver < 0) or (v.copper < 0):
            raise Exception(
                "Money amount cannot be negative for {}".format(info.field_name)
            )
        return v

    @field_validator("inventoryType", mode="before")
    def parse_inventory_type(cls, v: str, info: FieldValidationInfo) -> InventoryType:
        try:
            return InventoryType[v]
        except:
            raise Exception('"{}" is an invalid value for inventoryType'.format(v))

    @field_validator("quality", mode="before")
    def parse_quality(cls, v: str, info: FieldValidationInfo) -> Quality:
        try:
            return Quality[v]
        except:
            raise Exception('"{}" is an invalid value for quality'.format(v))

    @field_validator("bagFamily", mode="before")
    def parse_bag_family(cls, v: list[str], info: FieldValidationInfo) -> BagFamily:
        bag_families = vars(BagFamily)["__annotations__"].keys()
        bf = BagFamily()
        for item in v:
            if not item in bag_families:
                raise Exception("{} not a valid value for bagFamily".format(v))
            bf[item] = True
        return bf
