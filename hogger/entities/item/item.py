from enum import Enum, IntFlag
from textwrap import dedent
from typing import Literal

from mysql.connector.cursor_cext import CMySQLCursor as Cursor
from pydantic import (
    Field,
    FieldValidationInfo,
    SerializationInfo,
    field_serializer,
    field_validator,
)

from .item_spells import spells_from_sql
from hogger.entities import Entity
from hogger.entities.item import *
from hogger.types import *
from hogger.types import EnumUtils, LookupID, Money
from hogger.util import from_sql, to_sql

_enum_fields = [
    "ammoType",
    "bonding",
    "foodType",
    "inventoryType",
    "itemClass",
    "material",
    "quality",
    "sheath",
    "totemCategory",
]

_intflag_fields = [
    "bagFamily",
    "flags",
    "flagsCustom",
    "flagsExtra",
]

_enum_map_fields = [
    "resistances",
    "stats",
]


class Item(Entity, extra="allow"):
    type: Literal["Item"] = "Item"

    id: int = Field(
        default=-1,
        description=dedent(
            """
            Identifier for the item in the world database. Set to -1 to
            automagically use the first item id it finds. Default is -1.
            If the id is defined, the item definition in the database will
            be pinned to the id defined, and will overwrite whatever entry
            has that id.
            """
        ),
        json_schema_extra={
            "from_sql": from_sql("entry"),
            "to_sql": to_sql("entry"),
        },
    )
    name: str = Field(
        description=dedent(
            """
            The name of the item.
            """
        ),
        json_schema_extra={
            "from_sql": from_sql("name"),
            "to_sql": to_sql("name"),
        },
    )
    tag: str = Field(
        default="",
        description=(
            "The contents of this field is appended to the contents of the "
            "`name` field to serve as an identifier for entities of this type. "
            "The name, tag, and item type will all be used to identify the "
            "entity."
        ),
    )
    description: str = Field(
        default="",
        description=dedent(
            """
            The description that appears in yellow letters at the bottom of
            the item tooltip. No description by default.
            """
        ),
        json_schema_extra={
            "from_sql": from_sql("description"),
            "to_sql": to_sql("description"),
        },
    )
    scriptName: str = Field(
        default="",
        description=dedent(
            """
            The name of the script that the item should use. No script by
            default.
            """
        ),
        json_schema_extra={
            "from_sql": from_sql("ScriptName"),
            "to_sql": to_sql("ScriptName"),
        },
    )
    itemClass: (ItemClass | int) = Field(
        default=ItemClass.TradeGoods,
        description=dedent(
            """
            The category the item belongs to; e.g. consumable, weapon, armor,
            etc.
            """
        ),
        json_schema_extra={
            "from_sql": EnumUtils.from_sql("class"),
            "to_sql": EnumUtils.to_sql("class"),
        },
    )
    itemSubclass: int = Field(
        default=0,
        description=dedent(
            """
            The subcategory the item belongs to, and is dependent upon the
            value of itemClass.
            """
        ),
        json_schema_extra={
            "from_sql": from_sql("subclass"),
            "to_sql": to_sql("subclass"),
        },
    )
    soundOverride: int = Field(
        default=-1,
        description=dedent(
            """
            Each weapon type plays a unique sound on impact, which can be
            overriden by the unique sound of a different weapon type.
            Use -1 to use the default sound for the item. Default is -1.
            """
        ),
        json_schema_extra={
            "from_sql": from_sql("SoundOverrideSubclass"),
            "to_sql": to_sql("SoundOverrideSubclass"),
        },
        ge=-1,
    )
    displayId: int = Field(
        default=0,
        description=dedent(
            """
            Controls both the model appearance and icon.
            """
        ),
        json_schema_extra={
            "from_sql": from_sql("displayid"),
            "to_sql": to_sql("displayid"),
        },
        ge=0,
    )
    quality: (Quality | int) = Field(
        default=Quality.Common,
        description=dedent(
            """
            The quality of the item; valid values are: Poor, Uncommon,
            Common, Rare, Epic, Legendary, Artifact, BoA.
            """
        ),
        json_schema_extra={
            "from_sql": EnumUtils.from_sql("Quality"),
            "to_sql": EnumUtils.to_sql("Quality"),
        },
    )
    buyCount: int = Field(
        default=1,
        description=dedent(
            """
            The size of the item stack when sold by vendors. If a vendor has
            a limited number of this item available, the vendor's inventory
            will increase by this number when the vendor list is refreshed
            (see npc.vendor.incrtime).
            """
        ),
        json_schema_extra={
            "from_sql": from_sql("BuyCount"),
            "to_sql": to_sql("BuyCount"),
        },
        ge=1,
    )
    buyPrice: Money = Field(
        default=Money(gold=0, silver=0, copper=0),
        description=dedent(
            """
            The cost to purchase this item form a vendor
            """
        ),
        json_schema_extra={
            "from_sql": Money.from_sql_copper("BuyPrice"),
            "to_sql": Money.to_sql_copper("BuyPrice"),
        },
    )
    # TODO: buyPriceExtra
    sellPrice: Money = Field(
        default=Money(gold=0, silver=0, copper=0),
        description=dedent(
            """
            The amount a vendor will purchase this item from you for.
            """
        ),
        json_schema_extra={
            "from_sql": Money.from_sql_copper("SellPrice"),
            "to_sql": Money.to_sql_copper("SellPrice"),
        },
    )
    inventoryType: (InventoryType | int) = Field(
        default=InventoryType.NoEquip,
        description=dedent(
            """
            Is the item equippable? A quest item?
            """
        ),
        json_schema_extra={
            "from_sql": EnumUtils.from_sql("InventoryType"),
            "to_sql": EnumUtils.to_sql("InventoryType"),
        },
    )
    maxCount: int = Field(
        default=1,
        description=dedent(
            """
            The maximum amount that a player can have; use 0 for infinite.
            """
        ),
        json_schema_extra={
            "from_sql": from_sql("maxcount"),
            "to_sql": to_sql("maxcount"),
        },
        ge=0,
    )
    stackSize: int = Field(
        default=1,
        description=dedent(
            """
            The maximum size of a stack of this item.
            """
        ),
        json_schema_extra={
            "from_sql": from_sql("stackable"),
            "to_sql": to_sql("stackable"),
        },
        ge=1,
    )
    startsQuest: LookupID = Field(
        default=0,
        description=dedent(
            """
            The ID of the quest that this item will start if right-clicked.
            See quest_template.id.
            """
        ),
        json_schema_extra={
            "from_sql": from_sql("startquest"),
            "to_sql": to_sql("startquest"),
        },
    )
    # TODO: This could use a more intuitive name
    material: (Material | int) = Field(
        default=Material.Undefined,
        description=dedent(
            """
            Controls the sound played when moving items in your inventory.
            """
        ),
        json_schema_extra={
            "from_sql": EnumUtils.from_sql("Material"),
            "to_sql": EnumUtils.to_sql("Material"),
        },
    )
    randomStat: RandomStat = Field(
        default=RandomStat(),
        description=dedent(
            """
            Adds a random stat bonus on the item.
            """
        ),
        json_schema_extra={
            "from_sql": RandomStat.from_sql(
                RandomProperty="RandomProperty",
                RandomSuffix="RandomSuffix",
            ),
            "to_sql": RandomStat.to_sql(
                RandomProperty="RandomProperty",
                RandomSuffix="RandomSuffix",
            ),
        },
    )
    bagFamily: list[BagFamily | int] = Field(
        default=[],
        description=dedent(
            """
            Dictates what kind of bags this item can be placed in.
            """
        ),
        json_schema_extra={
            "from_sql": IntFlagUtils.from_sql("BagFamily"),
            # "to_sql": IntFlagUtils.to_sql("BagFamily"),
        },
    )
    containerSlots: int = Field(
        default=0,
        description=dedent(
            """
            If this item is a bag, controls the number of slots it will have
            """
        ),
        json_schema_extra={
            "from_sql": from_sql("ContainerSlots"),
            "to_sql": to_sql("ContainerSlots"),
        },
    )
    totemCategory: (TotemCategory | int) = Field(
        default=TotemCategory.Undefined,
        description=dedent(
            """
            Some items are required to complete certain tasks, such as a
            shaman's totems, blacksmithing hammers, or enchanting rods.
            """
        ),
        json_schema_extra={
            "from_sql": EnumUtils.from_sql("TotemCategory"),
            "to_sql": EnumUtils.to_sql("TotemCategory"),
        },
    )
    duration: Duration = Field(
        default=Duration(),
        description=dedent(
            """
            The amount of time an item will exist in a player's inventory
            before disappearing; setting the duration to 0 seconds will
            prevent the item from every disappearing.
            """
        ),
        json_schema_extra={
            "from_sql": Duration.from_sql_seconds("duration"),
            # "to_sql": Duration.to_sql_seconds("duration"),
        },
    )
    itemLimitCategory: LookupID = Field(
        default=0,
        description=dedent(
            """
            Defines if an item belongs to a "category", like "Mana Gems" or
            Healthstone" and it defines how many items of the category you
            can have in the bag (this is the "limit"). For example, for
            Healthstone, there are several items like Lesser Healthstone,
            Greater Healthstone, etc. but you can have only one in your bag
            (check as example value 3 or 4).
            """
        ),
        json_schema_extra={
            "from_sql": from_sql("ItemLimitCategory"),
            "to_sql": to_sql("ItemLimitCategory"),
        },
    )
    disenchantId: LookupID = Field(
        default=0,
        description=dedent(
            """
            Corresponds to an entry in disenchant_loot_template.
            """
        ),
        json_schema_extra={
            "from_sql": from_sql("DisenchantID"),
            "to_sql": to_sql("DisenchantID"),
        },
    )
    foodType: (FoodType | int) = Field(
        default=FoodType.Undefined,
        description=dedent(
            """
            Determines the category a fooditem falls into, if any. This is
            primarily used to determine what items hunter pet's will eat.
            Defaults to "Undefined".
            """
        ),
        json_schema_extra={
            "from_sql": EnumUtils.from_sql("FoodType"),
            "to_sql": EnumUtils.to_sql("FoodType"),
        },
    )
    minMoneyLoot: Money = Field(
        default=Money(),
        description=dedent(
            """
            Minimum amount of money contained in the item. If an item should
            not contain money, use Money(gold=0, silver=0, copper=0), which
            is the default for this field.
            """
        ),
        json_schema_extra={
            "from_sql": Money.from_sql_copper("minMoneyLoot"),
            "to_sql": Money.to_sql_copper("minMoneyLoot"),
        },
    )
    maxMoneyLoot: Money = Field(
        default=Money(),
        description=dedent(
            """
            Max amount of money contained in the item. If an item should
            not contain money, use Money(gold=0, silver=0, copper=0), which
            is the default for this field.
            """
        ),
        json_schema_extra={
            "from_sql": Money.from_sql_copper("maxMoneyLoot"),
            "to_sql": Money.to_sql_copper("maxMoneyLoot"),
        },
    )
    itemSet: LookupID = Field(
        default=0,
        description=dedent(
            """
            The ID of the item set that this item belongs to.
            """
        ),
        json_schema_extra={
            "from_sql": from_sql("itemset"),
            "to_sql": to_sql("itemset"),
        },
    )
    bonding: (ItemBinding | int) = Field(
        default=ItemBinding.Never,
        description=dedent(
            """
            Determines if the item binds to the character. Defaults to Never.
            """
        ),
        json_schema_extra={
            "from_sql": EnumUtils.from_sql("bonding"),
            "to_sql": EnumUtils.to_sql("bonding"),
        },
    )
    flags: list[ItemFlag | int] = Field(
        default=[],
        description=dedent(
            """
            A collection of flags to modify the behavior of the item.
            """
        ),
        json_schema_extra={
            "from_sql": IntFlagUtils.from_sql("Flags"),
            # "to_sql": IntFlagUtils.to_sql("Flags"),
        },
    )
    flagsExtra: list[ItemFlagExtra | int] = Field(
        default=[],
        description=dedent(
            """
            A collection of flags to modify the behavior of the item.
            """
        ),
        json_schema_extra={
            "from_sql": IntFlagUtils.from_sql("FlagsExtra"),
            # "to_sql": IntFlagUtils.to_sql("FlagsExtra"),
        },
    )
    flagsCustom: list[ItemFlagExtra | int] = Field(
        default=[],
        description=dedent(
            """
            A collection of flags to modify the behavior of the item.
            """
        ),
        json_schema_extra={
            "from_sql": IntFlagUtils.from_sql("flagsCustom"),
            # "to_sql": IntFlagUtils.to_sql("flagsCustom"),
        },
    )
    readText: ItemText = Field(
        default=ItemText(),
        json_schema_extra={
            "from_sql": ItemText.from_sql(
                id="PageText",
                pageMaterial="PageMaterial",
                language="LanguageID",
            ),
            # "to_sql": ItemText.to_sql(
            #     id="PageText",
            #     pageMaterial="PageMaterial",
            #     language="LanguageID",
            # ),
        },
    )
    requires: Requires = Field(
        default=Requires(),
        description="",
        json_schema_extra={
            "from_sql": Requires.from_sql(),
            # "to_sql": Requires.to_sql(),
        },
    )
    # TODO: Add automatic item level calculation as default.
    itemLevel: int = Field(
        default=0,
        description=dedent(
            """
            The level of the item, not to be confused with the item required to
            equip or use the item.
            """
        ),
        json_schema_extra={
            "from_sql": from_sql("ItemLevel"),
            "to_sql": to_sql("ItemLevel"),
        },
    )
    unlocks: LookupID = Field(
        default=0,
        description=dedent(
            """
            The lock entry ID that this item (which serves as a key) is tied to.
            This field is used in key-door mechanics.
            """
        ),
        json_schema_extra={
            "from_sql": from_sql("lockid"),
            "to_sql": to_sql("lockid"),
        },
    )
    resistances: dict[(ItemResistance | int), int] = Field(
        default=dict(),
        description=dedent(
            """
            Item resistances.
            """
        ),
        json_schema_extra={
            "from_sql": EnumMapUtils.from_sql_named_fields(
                {
                    "holy_res": "Holy",
                    "fire_res": "Fire",
                    "nature_res": "Nature",
                    "frost_res": "Frost",
                    "shadow_res": "Shadow",
                    "arcane_res": "Arcane",
                },
            ),
            # "to_sql": EnumMapUtils.to_sql_named_fields(
            #     {
            #         "holy_res": "Holy",
            #         "fire_res": "Fire",
            #         "nature_res": "Nature",
            #         "frost_res": "Frost",
            #         "shadow_res": "Shadow",
            #         "arcane_res": "Arcane",
            #     },
            # ),
        },
    )
    scalingStatDistribution: int = Field(
        default=0,
        description=dedent(
            """
            Similar to Static Stats these are the Stats that grow along with the
            users level (mainly heirloom leveling gear) use like static stats.
            """
        ),
        json_schema_extra={
            "from_sql": from_sql("ScalingStatDistribution"),
            "to_sql": to_sql("ScalingStatDistribution"),
        },
    )
    scalingStatValue: int = Field(
        default=0,
        description=dedent(
            """
            Final (level 80) value of the scaling-stat
            """
        ),
        json_schema_extra={
            "from_sql": from_sql("ScalingStatValue"),
            "to_sql": to_sql("ScalingStatValue"),
        },
    )
    stats: dict[(ItemStat | int), int] = Field(
        # TODO: must include `statCount` in serialization
        default=dict(),
        description=dedent(
            """
            Stats applied to the item in key-value pairs.
            """
        ),
        json_schema_extra={
            "from_sql": EnumMapUtils.stats_from_sql_kvpairs(
                {
                    "stat_type1": "stat_value1",
                    "stat_type2": "stat_value2",
                    "stat_type3": "stat_value4",
                    "stat_type5": "stat_value5",
                    "stat_type6": "stat_value6",
                    "stat_type7": "stat_value7",
                    "stat_type8": "stat_value8",
                    "stat_type9": "stat_value9",
                    "stat_type10": "stat_value10",
                },
            ),
            # "to_sql": EnumMapUtils.stats_to_sql_kvpairs(
            #     {
            #         "stat_type1": "stat_value1",
            #         "stat_type2": "stat_value2",
            #         "stat_type3": "stat_value4",
            #         "stat_type5": "stat_value5",
            #         "stat_type6": "stat_value6",
            #         "stat_type7": "stat_value7",
            #         "stat_type8": "stat_value8",
            #         "stat_type9": "stat_value9",
            #         "stat_type10": "stat_value10",
            #     },
            # ),
        },
    )
    sockets: ItemSockets = Field(
        default=ItemSockets(),
        description=dedent(
            """
            Item socket details.
            """
        ),
        json_schema_extra={
            "from_sql": ItemSockets.from_sql(),
            # "to_sql": ItemSockets.to_sql(),
        },
    )
    armor: int = Field(
        default=0,
        description=dedent(
            """
            The armor value of the item.
            """
        ),
        json_schema_extra={
            "from_sql": from_sql("armor"),
            "to_sql": to_sql("armor"),
        },
    )
    armorDamageModifier: int = Field(
        default=0,
        description=dedent(
            """
            This field is not well understood.
            """
        ),
        json_schema_extra={
            "from_sql": from_sql("ArmorDamageModifier"),
            "to_sql": to_sql("ArmorDamageModifier"),
        },
    )
    hitDelay: int = Field(
        default=0,
        description=dedent(
            """
            The time in milliseconds between successive hits.
            """
        ),
        json_schema_extra={
            "from_sql": from_sql("delay"),
            "to_sql": to_sql("delay"),
        },
    )
    ammoType: (AmmoType | int) = Field(
        default=AmmoType.Undefined,
        description=dedent(
            """
            The type of ammunition the item uses.
            """
        ),
        json_schema_extra={
            "from_sql": EnumUtils.from_sql("ammo_type"),
            "to_sql": EnumUtils.to_sql("ammo_type"),
        },
    )
    weaponRange: int = Field(
        default=0,
        description=dedent(
            """
            The range modifier for bows, crossbows, and guns.
            All of Blizzard's ranged weapons have a default range of 100.
            """
        ),
        json_schema_extra={
            "from_sql": from_sql("RangedModRange"),
            "to_sql": to_sql("RangedModRange"),
        },
    )
    block: int = Field(
        default=0,
        description=dedent(
            """
            If the item is a shield, this value will be the block chance of the
            shield.
            """
        ),
        json_schema_extra={
            "from_sql": from_sql("block"),
            "to_sql": to_sql("block"),
        },
    )
    durability: int = Field(
        default=100,
        description=dedent(
            """
            The durability of the item. Defaults to 100.
            """
        ),
        json_schema_extra={
            "from_sql": from_sql("MaxDurability"),
            "to_sql": to_sql("MaxDurability"),
        },
    )
    sheath: (Sheath | int) = Field(
        default=Sheath.Undefined,
        description=dedent(
            """
            Controls how the item is put away on the character. Press the 'Z'
            hotkey to sheath and unsheathe your weapons.
            """
        ),
        json_schema_extra={
            "from_sql": EnumUtils.from_sql("sheath"),
            "to_sql": EnumUtils.to_sql("sheath"),
        },
    )
    damage: Damage = Field(
        default=Damage(),
        description=dedent(
            """
            The damage values of the weapon.
            """
        ),
        json_schema_extra={
            "from_sql": Damage.from_sql(),
            # "to_sql": Damage.to_sql(),
        },
    )
    spells: list[ItemSpell] = Field(
        default=[],
        description=dedent(
            """
            Items can be used to invoke spells.
            """
        ),
        json_schema_extra={
            "from_sql": spells_from_sql(
                [
                    {
                        "id": "spellid_1",
                        "trigger": "spelltrigger_1",
                        "charges": "spellcharges_1",
                        "procsPerMinute": "spellppmRate_1",
                        "cooldown": "spellcooldown_1",
                        "category": "spellcategory_1",
                        "cooldownCategory": "spellcategorycooldown_1",
                    },
                    {
                        "id": "spellid_2",
                        "trigger": "spelltrigger_2",
                        "charges": "spellcharges_2",
                        "procsPerMinute": "spellppmRate_2",
                        "cooldown": "spellcooldown_2",
                        "category": "spellcategory_2",
                        "cooldownCategory": "spellcategorycooldown_2",
                    },
                    {
                        "id": "spellid_3",
                        "trigger": "spelltrigger_3",
                        "charges": "spellcharges_3",
                        "procsPerMinute": "spellppmRate_3",
                        "cooldown": "spellcooldown_3",
                        "category": "spellcategory_3",
                        "cooldownCategory": "spellcategorycooldown_3",
                    },
                    {
                        "id": "spellid_4",
                        "trigger": "spelltrigger_4",
                        "charges": "spellcharges_4",
                        "procsPerMinute": "spellppmRate_4",
                        "cooldown": "spellcooldown_4",
                        "category": "spellcategory_4",
                        "cooldownCategory": "spellcategorycooldown_4",
                    },
                    {
                        "id": "spellid_5",
                        "trigger": "spelltrigger_5",
                        "charges": "spellcharges_5",
                        "procsPerMinute": "spellppmRate_5",
                        "cooldown": "spellcooldown_5",
                        "category": "spellcategory_5",
                        "cooldownCategory": "spellcategorycooldown_5",
                    },
                ],
            ),
            # "to_sql": spells_to_sql(
            #     [
            #         {
            #             "id": "spellid_1",
            #             "trigger": "spelltrigger_1",
            #             "charges": "spellcharges_1",
            #             "procsPerMinute": "spellppmRate_1",
            #             "cooldown": "spellcooldown_1",
            #             "category": "spellcategory_1",
            #             "cooldownCategory": "spellcategorycooldown_1",
            #         },
            #         {
            #             "id": "spellid_2",
            #             "trigger": "spelltrigger_2",
            #             "charges": "spellcharges_2",
            #             "procsPerMinute": "spellppmRate_2",
            #             "cooldown": "spellcooldown_2",
            #             "category": "spellcategory_2",
            #             "cooldownCategory": "spellcategorycooldown_2",
            #         },
            #         {
            #             "id": "spellid_3",
            #             "trigger": "spelltrigger_3",
            #             "charges": "spellcharges_3",
            #             "procsPerMinute": "spellppmRate_3",
            #             "cooldown": "spellcooldown_3",
            #             "category": "spellcategory_3",
            #             "cooldownCategory": "spellcategorycooldown_3",
            #         },
            #         {
            #             "id": "spellid_4",
            #             "trigger": "spelltrigger_4",
            #             "charges": "spellcharges_4",
            #             "procsPerMinute": "spellppmRate_4",
            #             "cooldown": "spellcooldown_4",
            #             "category": "spellcategory_4",
            #             "cooldownCategory": "spellcategorycooldown_4",
            #         },
            #         {
            #             "id": "spellid_5",
            #             "trigger": "spelltrigger_5",
            #             "charges": "spellcharges_5",
            #             "procsPerMinute": "spellppmRate_5",
            #             "cooldown": "spellcooldown_5",
            #             "category": "spellcategory_5",
            #             "cooldownCategory": "spellcategorycooldown_5",
            #         },
            #     ],
            # ),
        },
    )
    build: int = Field(
        default=0,
        description="Indicates the build version that the item was added in.",
        json_schema_extra={
            "from_sql": from_sql("VerifiedBuild"),
            "to_sql": to_sql("VerifiedBuild"),
        },
    )

    @field_validator(*_enum_fields, mode="before")
    def parse_enum(cls, v: (str | int), info: FieldValidationInfo) -> Enum | int:
        return EnumUtils.parse(cls, v, info)

    @field_serializer(*_enum_fields, when_used="json")
    def serialize_enum_json(
        self, v: (Enum | int), info: SerializationInfo
    ) -> str | int:
        return EnumUtils.serialize(self, v, info)

    @field_validator(*_intflag_fields, mode="before")
    def parse_intflag(
        cls, items: list[str | int], info: FieldValidationInfo
    ) -> list[IntFlag | int]:
        return IntFlagUtils.parse(cls, items, info)

    @field_serializer(*_intflag_fields, when_used="json")
    def serialize_intflag(
        self, items: list[int | IntFlag], info: SerializationInfo
    ) -> list[str | int]:
        return IntFlagUtils.serialize(self, items, info)

    @field_validator(*_enum_map_fields, mode="before")
    def parse_enum_map(
        cls, dmap: dict[str, int], info: SerializationInfo
    ) -> dict[Enum, int]:
        return EnumMapUtils.parse(cls, dmap, info)

    @field_serializer(*_enum_map_fields, when_used="json")
    def serialize_enum_map(
        self, items: dict[(Enum | int), int], info: SerializationInfo
    ) -> dict[(str | int), int]:
        return EnumMapUtils.serialize(self, items, info)
    
    def db_key(self) -> int:
        return self.id

    def hogger_identifier(self) -> str:
        tag = self.tag.strip()
        suffix = ""
        if len(tag) > 0:
            suffix = f"#{tag}"
        return f"{self.name}{suffix}"

    @staticmethod
    def from_hoggerstate(
        db_key: int,
        hogger_identifier: str,
        cursor: Cursor,
    ) -> "Item":
        cursor.execute(
            f"""
            SELECT * FROM item_template
            WHERE entry={db_key};
            """
        )
        entity = cursor.fetchall()
        assert len(entity) == 1

        item_args = {}
        sql_dict = dict(zip(cursor.column_names, entity[0]))
        for field, field_properties in Item.model_fields.items():
            json_schema_extra = field_properties.json_schema_extra
            if json_schema_extra is not None and "from_sql" in json_schema_extra:
                from_sql_func = json_schema_extra["from_sql"]
                item_args[field] = from_sql_func(
                    sql_dict=sql_dict,
                    cursor=cursor,
                    field_type=field_properties.annotation,
                )

        item_args["type"] = "Item"

        tmp = sql_dict["name"].split("#")
        if len(tmp) == 1:
            tmp.append("")
        item_args["tag"] = tmp[1]
        return Item(**item_args)


    def diff(self, other: "Item") -> ("Item", dict[str, any]):
        # Reuse id of self if other is a negative number. This change won't be
        # shown in the diff, because it's an implied feature of the Item entity.
        if self.id <= -1:
            self.id = other.id

        diffs = {}
        desired = self.model_dump()
        actual = other.model_dump()

        for field in Item.model_fields:
            if desired[field] != actual[field]:
                diffs[field] = {
                    "desired": desired[field],
                    "actual": actual[field],
                }
                other.__setattr__(field, desired[field])
        return other, diffs


    def apply(self, cursor: Cursor) -> None:
        args = {}
        model_dict = self.model_dump()
        for field, field_properties in Item.model_fields.items():
            json_schema_extra = field_properties.json_schema_extra
            if json_schema_extra is not None and "to_sql" in json_schema_extra:
                to_sql_func = json_schema_extra["to_sql"]
                args = args | to_sql_func(
                    model_field=field,
                    model_dict=model_dict,
                    cursor=cursor,
                    field_type=field_properties.annotation,
                )

        print(tuple(args.keys()))
        print(tuple(args.values()))
        # for k, v in args.items():
        #     print(k, v) 
        # cursor.execute
        #     f"REPLACE INTO hoggerstate ()"
        #     "VALUES"
        # )
        # self._cnx.commit()
        print()
        return None
