from enum import IntFlag, auto


class BagFamily(IntFlag):
    Arrows: int = auto()
    Bullets: int = auto()
    SoulShards: int = auto()
    Leatherworking: int = auto()
    Inscription: int = auto()
    Herbs: int = auto()
    Enchanting: int = auto()
    Engineering: int = auto()
    Keys: int = auto()
    Gems: int = auto()
    Mining: int = auto()
    SoulboundEquipment: int = auto()
    VanityPets: int = auto()
    CurrencyTokens: int = auto()
    QuestItems: int = auto()


class ItemFlag(IntFlag):
    NoPickup: int = auto()
    Conjured: int = auto()
    HasLoot: int = auto()
    IsHeroic: int = auto()
    Deprecated: int = auto()
    NoUserDestroy: int = auto()
    PlayerCast: int = auto()
    NoEquipCooldown: int = auto()
    MultiLootQuest: int = auto()
    IsWrapper: int = auto()
    UsesResources: int = auto()
    MultiDrop: int = auto()
    ItemPurchaseRecord: int = auto()
    Petition: int = auto()
    HasText: int = auto()
    NoDisenchant: int = auto()
    RealDuration: int = auto()
    NoCreator: int = auto()
    IsProspectable: int = auto()
    UniqueEquippable: int = auto()
    IgnoreForAuras: int = auto()
    IgnoreDefaultArenaRestrictions: int = auto()
    NoDurabilityLoss: int = auto()
    UseWhenShapeshifted: int = auto()
    HasQuestGlow: int = auto()
    HideUnusableRecipe: int = auto()
    NotUsableInArena: int = auto()
    IsBoundToAccount: int = auto()
    NoReagentCost: int = auto()
    IsMillable: int = auto()
    ReportToGuildChat: int = auto()
    NoProgressiveLoot: int = auto()


class ItemFlagExtra(IntFlag):
    HordeOnly: int = 1
    AllianceOnly: int = 2
    ExtendedVendorCost: int = 4
    NeedRollDisabled: int = 16


class ItemFlagCustom(IntFlag):
    GlobalDuration: int = auto()
    IgnoreQuestStatus: int = auto()
    FollowLootRules: int = auto()

