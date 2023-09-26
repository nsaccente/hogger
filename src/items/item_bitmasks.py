import abc
from pydantic import BaseModel


class Bitmask(abc.ABC, BaseModel):
    def __setitem__(self, key, value):
        setattr(self, key, value)

    def __getitem__(self, key):
        return getattr(self, key)


class BagFamily(Bitmask):
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

class ItemFlags(Bitmask):
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


class ItemFlags(Bitmask):
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
    # honor points, emblems, armor tokens etc. defined in ItemExtendedCost.dbc
    AdditionalCost: bool = False 
    NeedRollDisabled: bool = False

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

