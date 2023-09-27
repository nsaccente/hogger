from enum import IntFlag


class BagFamily(IntFlag):
    Arrows: int = 0
    Bullets: int = 1
    SoulShards: int = 2
    Leatherworking: int = 3
    Inscription: int = 4
    Herbs: int = 5
    Enchanting: int = 6
    Engineering: int = 7
    Keys: int = 8
    Gems: int = 9
    Mining: int = 10
    SoulboundEquipment: int = 11
    VanityPets: int = 12
    CurrencyTokens: int = 13
    QuestItems: int = 14


class ItemFlag(IntFlag):
    NoPickup: int = 0
    Conjured: int = 1
    HasLoot: int = 2
    IsHeroic: int = 3
    Deprecated: int = 4
    NoUserDestroy: int = 5 
    PlayerCast: int = 6
    NoEquipCooldown: int = 7
    MultiLootQuest: int = 8
    IsWrapper: int = 9
    UsesResources: int = 10
    MultiDrop: int = 11
    ItemPurchaseRecord: int = 12
    Petition: int = 13
    HasText: int = 14
    NoDisenchant: int = 15
    RealDuration: int = 16
    NoCreator: int = 17
    IsProspectable: int = 18
    UniqueEquippable: int = 19
    IgnoreForAuras: int = 20
    IgnoreDefaultArenaRestrictions: int = 21
    NoDurabilityLoss: int = 22
    UseWhenShapeshifted: int = 23
    HasQuestGlow: int = 24
    HideUnusableRecipe: int  = 25
    NotUsableInArena: int = 26
    IsBoundToAccount: int = 27
    NoReagentCost: int = 28
    IsMillable: int = 29
    ReportToGuildChat: int = 30
    NoProgressiveLoot: int = 31


class ItemFlagExtra(IntFlag):
    HordeOnly: int = 0
    AllianceOnly: int = 1
    ExtendedVendorCost: int = 2
    NeedRollDisabled: int = 4


class ItemFlagCustom(IntFlag):
    GlobalDuration: int = 0
    IgnoreQuestStatus: int = 1
    FollowLootRules: int = 2


class AllowableClasses(IntFlag):
    Warrior: int = 0
    Paladin: int = 1
    Hunter: int = 2
    Rogue: int = 3
    Priest: int = 4
    DeathKnight: int = 5
    Shaman: int = 6
    Mage: int = 7
    Warlock: int = 8
    # UNDEFINED: int = 9
    Druid: int = 10