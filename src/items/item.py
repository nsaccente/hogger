import abc
import typing
from inspect import cleandoc

from pydantic import (BaseModel, Field, FieldValidationInfo, SerializationInfo,
                      field_serializer, field_validator)

from src.misc import Duration, Money

from .item_enums import *
from .item_damage import *
from .item_flags import *
from .item_sockets import *
from .item_randomstat import *
from src.misc.currency import LookupID


class Item(BaseModel, abc.ABC):
    # MISCELLANEOUS
    id: int = Field(
        default=-1,
        description=cleandoc(
            """
            Identifier for the item in the world database. Set to -1 to
            automagically use the first item id it finds. Default is -1.
            If the id is defined, the item definition in the database will
            be pinned to the id defined, and will overwrite whatever entry
            has that id.
            """
        ),
        serialization_alias="entry",
    )
    id_offset: int = Field(
        default=60000,
        description=cleandoc(
            """
            Dictates the first id the item is allowed to use. This allows
            separation of custom items and vanilla items.
            """
        ),
        exclude=True,
        ge=0,
    )
    name: str = Field(
        description=cleandoc(
            """
            The name of the item.
            """
        ),
    )
    description: str = Field(
        default="",
        description=cleandoc(
            """
            The description that appears in yellow letters at the bottom of
            the item tooltip. No description by default.
            """
        ),
    )
    scriptName: str = Field(
        default="",
        description=cleandoc(
            """
            The name of the script that the item should use. No script by
            default.
            """
        ),
        serialization_alias="ScriptName",
    )
    itemClass: ItemClass = Field(
        default=ItemClass.TradeGoods,
        description=cleandoc(
            """
            The category the item belongs to; e.g. consumable, weapon, armor,
            etc.
            """
        ),
        serialization_alias="class",
    )
    itemSubclass: int = Field(
        defalt=0,
        description=cleandoc(
            """
            The subcategory the item belongs to, and is dependent upon the
            value of itemClass.
            """
        ),
        serialization_alias="subclass",
    )
    soundOverride: int = Field(
        default=-1,
        description=cleandoc(
            """
            Each weapon type plays a unique sound on impact, which can be
            overriden by the unique sound of a different weapon type.
            Use -1 to use the default sound for the item. Default is -1.
            """
        ),
        serialization_alias="SoundOverrideSubclass",
        ge=-1,
    )
    displayId: int = Field(
        default=0,
        description=cleandoc(
            """
            Controls both the model appearance and icon.
            """
        ),
        serialization_alias="displayid",
        ge=0,
    )
    quality: Quality = Field(
        default=Quality.Common,
        description=cleandoc(
            """
            The quality of the item; valid values are: Poor, Uncommon,
            Common, Rare, Epic, Legendary, Artifact, BoA.
            """
        ),
        serialization_alias="Quality",
    )
    buyCount: int = Field(
        default=1,
        description=cleandoc(
            """
            The size of the item stack when sold by vendors. If a vendor has
            a limited number of this item available, the vendor's inventory
            will increase by this number when the vendor list is refreshed
            (see npc.vendor.incrtime).
            """
        ),
        serialization_alias="BuyCount",
        ge=1,
    )
    buyPrice: Money = Field(
        default=Money(gold=0, silver=0, copper=0),
        description=cleandoc(
            """
            The cost to purchase this item form a vendor
            """
        ),
        serialization_alias="BuyPrice",
    )
    #buyPriceExtra
    sellPrice: Money = Field(
        default=Money(gold=0, silver=0, copper=0),
        description=cleandoc(
            """
            The amount a vendor will purchase this item from you for.
            """
        ),
        serialization_alias="SellPrice",
    )
    inventoryType: InventoryType = Field(
        default=InventoryType.NoEquip,
        description=cleandoc(
            """
            Is the item equippable? A quest item?
            """
        ),
        serialization_alias="InventoryType",
    )
    maxCount: int = Field(
        default=1,
        description=cleandoc(
            """
            The maximum amount that a player can have; use 0 for infinite.
            """
        ),
        serialization_alias="maxcount",
        ge=0,
    )
    stackSize: int = Field(
        default=1,
        description=cleandoc(
            """
            The maximum size of a stack of this item.
            """
        ),
        serialization_alias="stackable",
        ge=1,
    )
    startsQuest: LookupID = Field(
        default=0,
        description=(
            """
            The ID of the quest that this item will start if right-clicked.
            See quest_template.id.
            """
        ),
        serialization_alias="startquest",
    )
    material: Material = Field(
        default=Material.Undefined,
        description=cleandoc(
            """
            Controls the sound played when moving items in your inventory.
            """
        ),
        serialization_alias="Material",
    )
    randomStat: RandomStat = Field(
        default = RandomStat(),
        description=(
            """
            Adds a random stat bonus on the item.
            """
        ),
    )
    bagFamily: list[BagFamily | int] = Field(
        default=[],
        description=cleandoc(
            """
            Dictates what kind of bags this item can be placed in.
            """
        ),
        serialization_alias="BagFamily",
    )
    containerSlots: int = Field(
        default=0,
        description=cleandoc(
            """
            If this item is a bag, controls the number of slots it will have
            """
        ),
        serialization_alias="ContainerSlots",
    )
    totemCategory: TotemCategory = Field(
        default=TotemCategory.Undefined,
        description=cleandoc(
            """
            Some items are required to complete certain tasks, such as a
            shaman's totems, blacksmithing hammers, or enchanting rods.
            """
        ),
        serialization_alias="TotemCategory",
    )
    duration: Duration = Field(
        default=Duration(),
        description=cleandoc(
            """
            The amount of time an item will exist in a player's inventory
            before disappearing; setting the duration to 0 seconds will
            prevent the item from every disappearing.
            """
        ),
    )
    itemLimitCategory: LookupID = Field(
        default=0,
        description=cleandoc(
            """
            Defines if an item belongs to a "category", like "Mana Gems" or
            Healthstone" and it defines how many items of the category you
            can have in the bag (this is the "limit"). For example, for
            Healthstone, there are several items like Lesser Healthstone,
            Greater Healthstone, etc. but you can have only one in your bag
            (check as example value 3 or 4).
            """
        ),
        serialization_alias="ItemLimitCategory",
    )

    # ENCHANTING ~~~~~~~~~~~~~~~~~
    # TODO: Create dedicated DisenchantID Class
    disenchantId: LookupID = Field(
        default=0,
        description=cleandoc(
            """
            Corresponds to an entry in disenchant_loot_template.
            """
        ),
        serialization_alias="DisenchantID",
    )
    disenchantSkill: int = Field(
        default=-1,
        description=cleandoc(
            """
            The required skill proficiency in disenchanting that the player must
            have in order to disenchant this item.
            """
        ),
        serialization_alias="",
        ge=-1,
    )
    foodType: FoodType = Field(
        default=FoodType.Undefined,
        description=cleandoc(
            """
            Determines the category a fooditem falls into, if any. This is
            primarily used to determine what items hunter pet's will eat.
            Defaults to "Undefined".
            """
        ),
        serialization_alias="FoodType",
    )
    minMoneyLoot: Money = Field(
        default=Money(),
        description=cleandoc(
            """
            Minimum amount of money contained in the item. If an item should
            not contain money, use Money(gold=0, silver=0, copper=0), which
            is the default for this field.
            """
        ),
    )
    maxMoneyLoot: Money = Field(
        default=Money(),
        description=cleandoc(
            """
            Max amount of money contained in the item. If an item should
            not contain money, use Money(gold=0, silver=0, copper=0), which
            is the default for this field.
            """
        ),
    )
    itemSet: LookupID = Field(
        default=0,
        description=cleandoc(
            """
            The ID of the item set that this item belongs to.
            """
        ),
        ge=0,
        serialization_alias="itemset",
    )
    bonding: ItemBinding = Field(
        default=ItemBinding.Never,
        description=cleandoc(
            """
            Determines if the item binds to the character. Defaults to Never.
            """
        ),
    )

    # FLAGS
    flags: list[ItemFlag | int] = Field(
        default=[],
        description=cleandoc(
            """
            A collection of flags to modify the behavior of the item.
            """
        ),
    )
    flagsExtra: list[ItemFlagExtra | int] = Field(
        default=[],
        description=cleandoc(
            """
            A collection of flags to modify the behavior of the item.
            """
        ),
    )
    flagsCustom: list[ItemFlagExtra | int] = Field(
        default=[],
        description=cleandoc(
            """
            A collection of flags to modify the behavior of the item.
            """
        ),
    )

    # TEXTS
    pageText: LookupID = Field(
        default=0,
        description=cleandoc(
            """
            The ID of the row in the `page_text` table corresponding to the text
            that will be shown to the player.
            """
        ),
        ge=0
    )
    pageMaterial: PageMaterial = Field(
        default=PageMaterial.Parchment,
        description=cleandoc(
            """
            The material that the text will be displayed on to the player.
            Defaults to parchment.
            """
        ),
    )
    language: (Language | LookupID) = Field(
        default=Language.Universal,
        description=cleandoc(
            """
            The RPG language that the document will be written in, requiring 
            players to be fluent in the document's language in order to read
            it correctly. Defaults to Universal, meaning all players will be
            able to interpret it, with no language requirements.
            """
        )
    )

    # REQUIREMENTS
    classes: list[AllowableClass | int] = Field(
        default=[],
        description=cleandoc(
            """
            Classes permitted to use the item.
            """
        ),
        serialization_alias="AllowableClass",
    )
    races: list[AllowableRace | int] = Field(
        default=[],
        description=cleandoc(
            """
            Races permitted to use the item.
            """
        ),
        serialization_alias="AllowableRace",
    )
    itemLevel: int = Field(
        # TODO: Add automatic item level calculation as default.
        default=0,
        description=cleandoc(
            """
            The level of the item, not to be confused with the item required to
            equip or use the item.
            """
        ),
        serialization_alias="ItemLevel",
        ge=0,
    )
    requiredLevel: int = Field(
        default=1,
        descrption=cleandoc(
            """
            The minimum player level required to equip the item.
            """
        ),
        serialization_alias="RequiredLevel",
        ge=1,
    )
    # requiredSkill: Lookup = Field(

    # )
    # requiredSkillRank:
    # RequiredSpell
    requiredHonorRank: RequiredHonorRank = Field(
        default=RequiredHonorRank.Undefined,
        description=cleandoc(
            """
            The required PvP rank required to use the item.",
            serialization_alias="requiredhonorrank",
            """
        ),
    )
    requiredCityRank: int = Field(
        default=0,
        description=cleandoc(
            """
            Unused. All items have this set to 0.
            """
        ),
        serialization_alias="RequiredCityRank",
        ge=0,
    )

    # TODO: Composite object here.
    # requiredRepFaction
    # RequiredRepRank

    # map
    # area
    # requiredHoliday
    # lock_id

    # RESISTANCE
    resistances: dict[ItemResistance, int] = Field(
        default=dict(),
        description=cleandoc(
            """
            Item resistances.
            """
        ),
    )

    # STATS
    # ScalingStatDistribution: int
    # ScalingStatValue: int
    statCount: int = Field(
        default=0,
        description=cleandoc(
            """
            The total number of stats attached to this item. Defaults to 0.
            """
        ),
        ge=0,
    )
    stats: dict[ItemStat, int] = Field(
        default=dict(),
        description=cleandoc(
            """
            Stats applied to the item in key-value pairs.
            """
        ),
    )

    # SOCKETS
    sockets: ItemSockets = Field(
        default=ItemSockets(),
        description=cleandoc(
            """
            Item socket details.
            """
        ),
    )

    # WEAPON ARMOR
    armor: int = Field(
        default=0,
        description=cleandoc(
            """
            The armor value of the item.
            """
        ),
    )
    armorDamageModifier: int = Field(
        default=0,
        description=cleandoc(
            """
            This field is not well understood.
            """
        ),
    )
    hitDelay: int = Field(
        default=0,
        description=cleandoc(
            """
            The time in milliseconds between successive hits.
            """
        ),
        ge=0,
    )
    ammoType: AmmoType = Field(
        default=AmmoType.Undefined,
        description=cleandoc(
            """
            The type of ammunition the item uses.
            """
        ),
    )
    weaponRange: int = Field(
        default=0,
        description=cleandoc(
            """
            The range modifier for bows, crossbows, and guns.
            All of Blizzard's ranged weapons have a default range of 100.
            """
        ),
        ge=0,
    )
    block: int = Field(
        default=0,
        description=cleandoc(
            """
            If the item is a shield, this value will be the block chance of the
            shield.
            """
        ),
    )
    durability: int = Field(
        default=100,
        description=cleandoc(
            """
            The durability of the item. Defaults to 100.
            """
        ),
        ge=0,
    )
    damage: Damage = Field(
        default=Damage(),
        description=cleandoc(
            """
            The damage values of the weapon.
            """
        ),
    )

    # ItemSpells

    @field_validator(
        "bonding",
        "foodType",
        "inventoryType",
        "language",
        "material",
        "quality",
        "totemCategory",
        mode="before",
    )
    def parse_enum(cls, v: str, info: FieldValidationInfo) -> Enum:
        field_type = typing.get_type_hints(cls)[info.field_name]
        try:
            return field_type[v]
        except:
            raise Exception(
                f'"{v}" is an invalid value for field "{field_type.__name__}"',
            )

    @field_serializer(
        "bonding",
        "foodType",
        "inventoryType",
        "language",
        "material",
        "quality",
        "totemCategory",
        when_used="unless-none",
    )
    def serialize_enum(self, v: Enum, info: SerializationInfo) -> str:
        if isinstance(v, Enum):
            return v.name
        return v

    @field_validator(
        "bagFamily",
        "classes",
        "flags",
        "flagsCustom",
        "flagsExtra",
        "races",
        mode="before",
    )
    def parse_intflag(
        cls, items: list[str | int], info: FieldValidationInfo
    ) -> list[IntFlag | int]:
        intflag_type = list(
            filter(
                lambda field_type: (issubclass(field_type, IntFlag)),
                (
                    typing.get_type_hints(cls)[info.field_name]
                    .__args__[0]  # args passed to list[]
                    .__args__  # args passed to Union[]
                ),
            )
        )[  # convert the elements returned by filter to a list
            0
        ]  # grab the first element in the list.

        intflags = [i.value for i in intflag_type]
        result = []
        for item in items:
            if isinstance(item, str):
                try:
                    result.append(intflag_type[item])
                except:
                    raise Exception(
                        f'"{item}" not a valid value for "{intflag_type.__name__}'
                    )
            elif isinstance(item, int):
                flag = 2**item
                if flag in intflags:
                    result.append(intflag_type(int(2**item)))
                else:
                    result.append(int(item))
            elif issubclass(IntFlag, item):
                result.append(item)

        return result

    @field_serializer(
        "bagFamily",
        "classes",
        "flags",
        "flagsCustom",
        "flagsExtra",
        "races",
        when_used="unless-none",
    )
    def serialize_intflag(
        self, items: list[int | IntFlag], info: SerializationInfo
    ) -> list[str | int]:
        result = []
        for item in items:
            if issubclass(type(item), IntFlag):
                result.append(item.name)
            else:
                result.append(item)
        return result

    @field_validator(
        "resistances",
        "stats",
        mode="before",
    )
    def parse_enum_map(
        cls, dmap: dict[str, int], info: SerializationInfo
    ) -> dict[Enum, int]:
        enum_type = typing.get_type_hints(cls)[info.field_name].__args__[0]
        if enum_type == ItemStat and len(dmap) > 10:
            raise Exception(
                f"Provided {len(dmap)} stats, cannot exceed 10.",
            )
        elif enum_type == ItemResistance and len(dmap) > 6:
            raise Exception(
                f"Provided {len(dmap)} resistances, cannot exceed 6.",
            )
        return {enum_type[k]: v for k, v in dmap.items()}

    @field_serializer(
        "resistances",
        "stats",
        when_used="unless-none",
    )
    def serialize_enum_map(
        self, items: dict[Enum, int], info: SerializationInfo
    ) -> dict[str, int]:
        return {str(k.name): v for k, v in items.items()}


#     def to_sql(self) -> str:
#         m = self.model_dump(by_alias=True)
#         sql_fields = cleandoc(
#             f"""DELETE FROM `item_template` WHERE (`entry` = {m["entry"]});
#                 INSERT INTO `item_template` (
#             """
#         )
#         sql_values = ")\nVALUES ("

#         for k, v in m.items():
#             if isinstance(v, str):
#                 v = f"'{v}'"
#             # elif isinstance(v, Money):
#             #     print(v)
#                 # v = int(v)
#             sql_fields += f"{k}, "
#             sql_values += f"{v},"
#         return f"{sql_fields}\n{sql_values})"
#         DELETE FROM `item_template` WHERE (`entry` = 38);
# INSERT INTO `item_template` (`entry`, `class`, `subclass`, `SoundOverrideSubclass`, `name`, `displayid`, `Quality`, `Flags`, `FlagsExtra`, `BuyCount`, `BuyPrice`, `SellPrice`, `InventoryType`, `AllowableClass`, `AllowableRace`, `ItemLevel`, `RequiredLevel`, `RequiredSkill`, `RequiredSkillRank`, `requiredspell`, `requiredhonorrank`, `RequiredCityRank`, `RequiredReputationFaction`, `RequiredReputationRank`, `maxcount`, `stackable`, `ContainerSlots`, `StatsCount`, `stat_type1`, `stat_value1`, `stat_type2`, `stat_value2`, `stat_type3`, `stat_value3`, `stat_type4`, `stat_value4`, `stat_type5`, `stat_value5`, `stat_type6`, `stat_value6`, `stat_type7`, `stat_value7`, `stat_type8`, `stat_value8`, `stat_type9`, `stat_value9`, `stat_type10`, `stat_value10`, `ScalingStatDistribution`, `ScalingStatValue`, `dmg_min1`, `dmg_max1`, `dmg_type1`, `dmg_min2`, `dmg_max2`, `dmg_type2`, `armor`, `holy_res`, `fire_res`, `nature_res`, `frost_res`, `shadow_res`, `arcane_res`, `delay`, `ammo_type`, `RangedModRange`, `spellid_1`, `spelltrigger_1`, `spellcharges_1`, `spellppmRate_1`, `spellcooldown_1`, `spellcategory_1`, `spellcategorycooldown_1`, `spellid_2`, `spelltrigger_2`, `spellcharges_2`, `spellppmRate_2`, `spellcooldown_2`, `spellcategory_2`, `spellcategorycooldown_2`, `spellid_3`, `spelltrigger_3`, `spellcharges_3`, `spellppmRate_3`, `spellcooldown_3`, `spellcategory_3`, `spellcategorycooldown_3`, `spellid_4`, `spelltrigger_4`, `spellcharges_4`, `spellppmRate_4`, `spellcooldown_4`, `spellcategory_4`, `spellcategorycooldown_4`, `spellid_5`, `spelltrigger_5`, `spellcharges_5`, `spellppmRate_5`, `spellcooldown_5`, `spellcategory_5`, `spellcategorycooldown_5`, `bonding`, `description`, `PageText`, `LanguageID`, `PageMaterial`, `startquest`, `lockid`, `Material`, `sheath`, `RandomProperty`, `RandomSuffix`, `block`, `itemset`, `MaxDurability`, `area`, `Map`, `BagFamily`, `TotemCategory`, `socketColor_1`, `socketContent_1`, `socketColor_2`, `socketContent_2`, `socketColor_3`, `socketContent_3`, `socketBonus`, `GemProperties`, `RequiredDisenchantSkill`, `ArmorDamageModifier`, `duration`, `ItemLimitCategory`, `HolidayId`, `ScriptName`, `DisenchantID`, `FoodType`, `minMoneyLoot`, `maxMoneyLoot`, `flagsCustom`, `VerifiedBuild`) VALUES
# (38, 4, 0, -1, 'Recruit\'s Shirt', 9891, 1, 0, 0, 1, 1, 1, 4, -1, -1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0, 0, -1, 0, -1, 0, '', 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, '', 0, 0, 0, 0, 0, 12340);
