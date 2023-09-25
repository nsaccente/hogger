import abc
from enum import Enum

from pydantic import BaseModel, Field


class Bitmask(abc.ABC):
    def __setitem__(self, key, value):
        setattr(self, key, value)

    def __getitem__(self, key):
        return getattr(self, key)


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


class BagFamily(Bitmask, BaseModel):
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

    def __int__(self) -> int:
        return sum(
            (self.Arrows * 1),
            (self.Bullets * 2),
            (self.SoulShards * 4),
            (self.Leatherworking * 8),
            (self.Inscription * 16),
            (self.Herbs * 32),
            (self.Enchanting * 64),
            (self.Engineering * 128),
            (self.Keys * 256),
            (self.Gems * 512),
            (self.Mining * 1024),
            (self.SoulboundEquipment * 2048),
            (self.VanityPets * 4096),
            (self.CurrencyTokens * 8192),
            (self.QuestItems * 16384),
        )


class ItemLimitCategory(BaseModel):
    id: int = Field(
        default=0,
        validation_alias="ID",
    )
    name: str = Field(
        validation_alias="Name",
    )
    count: int = Field(
        default=1,
        validation_alias="Count",
    )
    isGem: bool = Field(default=False, validation_alias="IsGem")


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


class ItemFlags(Bitmask, BaseModel):
    NoPickup: bool = False
    Conjured: bool = False
    HasLoot: bool = False
    IsHeroic: bool = False
    Deprecated: bool = False
    NoUserDestroy: bool = False
    PlayerCast: bool = False
    NoEquipCooldown: bool = False
    MultiLootQuest: bool = False
    IsWrapper: bool = False
    UsesResources: bool = False
    MultiDrop: bool = False
    ItemPurchaseRecord: bool = False
    Petition: bool = False
    HasText: bool = False
    NoDisenchant: bool = False
    RealDuration: bool = False
    NoCreator: bool = False
    IsProspectable: bool = False
    UniqueEquippable: bool = False
    IgnoreForAuras: bool = False
    IgnoreDefaultArenaRestrictions: bool = False
    NoDurabilityLoss: bool = False
    UseWhenShapeshifted: bool = False
    HasQuestGlow: bool = False
    HideUnusableRecipe: bool = False
    NotUsableInArena: bool = False
    IsBoundToAccount: bool = False
    NoReagentCost: bool = False
    IsMillable: bool = False
    ReportToGuildChat: bool = False
    NoProgressiveLoot: bool = False

    HordeOnly: bool = False
    AllianceOnly: bool = False
    ExtendedVendorCost: bool = False
    NeedRollDisabled: bool = False
    # There's potentially more flags

    GlobalDuration: bool = False
    IgnoreQuestStatus: bool = False
    FollowLootRules: bool = False

    def __int__(self) -> tuple[int]:
        flags = 2 ** sum(
            (self.NoPickup * 0),
            (self.Conjured * 1),
            (self.HasLoot * 2),
            (self.IsHeroic * 3),
            (self.Deprecated * 4),
            (self.NoUserDestroy * 5),
            (self.PlayerCast * 6),
            (self.NoEquipCooldown * 7),
            (self.MultiLootQuest * 8),
            (self.IsWrapper * 9),
            (self.UsesResources * 10),
            (self.MultiDrop * 11),
            (self.ItemPurchaseRecord * 12),
            (self.Petition * 13),
            (self.HasText * 14),
            (self.NoDisenchant * 15),
            (self.RealDuration * 16),
            (self.NoCreator * 17),
            (self.IsProspectable * 18),
            (self.UniqueEquippable * 19),
            (self.IgnoreForAuras * 20),
            (self.IgnoreDefaultArenaRestrictions * 21),
            (self.NoDurabilityLoss * 22),
            (self.UseWhenShapeshifted * 23),
            (self.HasQuestGlow * 24),
            (self.HideUnusableRecipe * 25),
            (self.NotUsableInArena * 26),
            (self.IsBoundToAccount * 27),
            (self.NoReagentCost * 28),
            (self.IsMillable * 29),
            (self.ReportToGuildChat * 30),
            (self.NoProgressiveLoot * 31),
        )

        flags_extra = 2 ** sum(
            (self.HordeOnly * 1),
            (self.AllianceOnly * 2),
            (self.ExtendedVendorCost * 4),
        )

        flags_custom = 2 ** sum(
            (self.GlobalDuration * 0),
            (self.IgnoreQuestStatus * 1),
            (self.FollowLootRules * 2),
        )

        return (flags, flags_extra, flags_custom)


class ItemLimitCategory(BaseModel):
    id: int = Field(
        default=0,
        serialization_alias="ID",
    )
    name: str = Field(
        serialization_alias="Name",
    )
    count: int = Field(
        default=1,
        serialization_alias="Count",
    )
    isGem: bool = Field(
        default=False,
        serialization_alias="IsGem",
    )
