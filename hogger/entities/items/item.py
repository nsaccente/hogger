from enum import Enum, IntFlag
from typing import Literal
from textwrap import dedent

from pydantic import (
    Field,
    FieldValidationInfo,
    SerializationInfo,
    field_serializer,
    field_validator,
)

from hogger.entities import Entity
from hogger.entities.items import *
from hogger.util import *

from mysql.connector.cursor_cext import CMySQLCursor as Cursor


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

class Item(Entity):
    type: Literal["Item"]
    
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
        from_sql=direct_map("entry"),
    )
    name: str = Field(
        description=dedent(
            """
            The name of the item.
            """
        ),
        from_sql=direct_map("name"),
    )
    description: str = Field(
        default="",
        description=dedent(
            """
            The description that appears in yellow letters at the bottom of
            the item tooltip. No description by default.
            """
        ),
        from_sql=direct_map("description"),
    )
    scriptName: str = Field(
        default="",
        description=dedent(
            """
            The name of the script that the item should use. No script by
            default.
            """
        ),
        from_sql=direct_map("ScriptName"),
    )
    itemClass: (ItemClass | int) = Field(
        default=ItemClass.TradeGoods,
        description=dedent(
            """
            The category the item belongs to; e.g. consumable, weapon, armor,
            etc.
            """
        ),
        from_sql=EnumUtils.from_sql("class"),
    )
    itemSubclass: int = Field(
        defalt=0,
        description=dedent(
            """
            The subcategory the item belongs to, and is dependent upon the
            value of itemClass.
            """
        ),
        from_sql=direct_map("subclass"),
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
        from_sql=direct_map("SoundOverrideSubclass"),
        ge=-1,
    )
    displayId: int = Field(
        default=0,
        description=dedent(
            """
            Controls both the model appearance and icon.
            """
        ),
        from_sql=direct_map("displayid"),
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
        from_sql=EnumUtils.from_sql("Quality"),
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
        from_sql=direct_map("BuyCount"),
        ge=1,
    )
    buyPrice: Money = Field(
        default=Money(gold=0, silver=0, copper=0),
        description=dedent(
            """
            The cost to purchase this item form a vendor
            """
        ),
        from_sql=Money.from_sql_copper("BuyPrice"),
    )
    # TODO: buyPriceExtra
    sellPrice: Money = Field(
        default=Money(gold=0, silver=0, copper=0),
        description=dedent(
            """
            The amount a vendor will purchase this item from you for.
            """
        ),
        from_sql=Money.from_sql_copper("SellPrice"),
    )
    inventoryType: (InventoryType | int) = Field(
        default=InventoryType.NoEquip,
        description=dedent(
            """
            Is the item equippable? A quest item?
            """
        ),
        from_sql=EnumUtils.from_sql("InventoryType"),
    )
    maxCount: int = Field(
        default=1,
        description=dedent(
            """
            The maximum amount that a player can have; use 0 for infinite.
            """
        ),
        from_sql=direct_map("maxcount"),
        ge=0,
    )
    stackSize: int = Field(
        default=1,
        description=dedent(
            """
            The maximum size of a stack of this item.
            """
        ),
        from_sql=direct_map("stackable"),
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
        from_sql=direct_map("startquest"),
    )
    # TODO: This could use a more intuitive name
    material: (Material | int) = Field(
        default=Material.Undefined,
        description=dedent(
            """
            Controls the sound played when moving items in your inventory.
            """
        ),
        from_sql=direct_map("Material"),
    )
    randomStat: RandomStat = Field(
        default=RandomStat(),
        description=dedent(
            """
            Adds a random stat bonus on the item.
            """
        ),
        from_sql=RandomStat.from_sql(
            RandomProperty="RandomProperty",
            RandomSuffix="RandomSuffix",
        )
    )
    bagFamily: list[BagFamily | int] = Field(
        default=[],
        description=dedent(
            """
            Dictates what kind of bags this item can be placed in.
            """
        ),
        from_sql=IntFlagUtils.from_sql("BagFamily"),
    )
    containerSlots: int = Field(
        default=0,
        description=dedent(
            """
            If this item is a bag, controls the number of slots it will have
            """
        ),
        from_sql=direct_map("ContainerSlots"),
    )
    totemCategory: (TotemCategory | int) = Field(
        default=TotemCategory.Undefined,
        description=dedent(
            """
            Some items are required to complete certain tasks, such as a
            shaman's totems, blacksmithing hammers, or enchanting rods.
            """
        ),
        from_sql=EnumUtils.from_sql("TotemCategory"),
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
        from_sql=Duration.from_sql_seconds("duration"),
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
        from_sql=direct_map("ItemLimitCategory"),
    )
    disenchantId: LookupID = Field(
        default=0,
        description=dedent(
            """
            Corresponds to an entry in disenchant_loot_template.
            """
        ),
        from_sql=direct_map("DisenchantID"),
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
        from_sql=EnumUtils.from_sql("FoodType"),
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
        from_sql=Money.from_sql_copper("minMoneyLoot")
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
        from_sql=Money.from_sql_copper("maxMoneyLoot")
    )
    itemSet: LookupID = Field(
        default=0,
        description=dedent(
            """
            The ID of the item set that this item belongs to.
            """
        ),
        ge=0,
        from_sql=direct_map("itemset"),
    )
    bonding: (ItemBinding | int) = Field(
        default=ItemBinding.Never,
        description=dedent(
            """
            Determines if the item binds to the character. Defaults to Never.
            """
        ),
        from_sql=EnumUtils.from_sql("bonding"),
    )
    flags: list[ItemFlag | int] = Field(
        default=[],
        description=dedent(
            """
            A collection of flags to modify the behavior of the item.
            """
        ),
        from_sql=IntFlagUtils.from_sql("Flags"),
    )
    flagsExtra: list[ItemFlagExtra | int] = Field(
        default=[],
        description=dedent(
            """
            A collection of flags to modify the behavior of the item.
            """
        ),
        from_sql=IntFlagUtils.from_sql("FlagsExtra"),
    )
    flagsCustom: list[ItemFlagExtra | int] = Field(
        default=[],
        description=dedent(
            """
            A collection of flags to modify the behavior of the item.
            """
        ),
        from_sql=IntFlagUtils.from_sql("flagsCustom"),
    )
    readText: ItemText = Field(
        default=ItemText(),
        sql_fields=["PageText", "PageMaterial", "LanguageID"],
        from_sql=ItemText.from_sql(
            id="PageText",
            pageMaterial="PageMaterial",
            language="LanguageID",
        )
    )
    requires: Requires = Field(
        default=Requires(),
        description="",
        from_sql=Requires.from_sql()
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
        from_sql=direct_map("ItemLevel"),
    )
    unlocks: LookupID = Field(
        default=0,
        description=dedent(
            """
            The lock entry ID that this item (which serves as a key) is tied to.
            This field is used in key-door mechanics.
            """
        ),
        from_sql=direct_map("lockid"),
    )
    resistances: dict[(ItemResistance | int), int] = Field(
        default=dict(),
        description=dedent(
            """
            Item resistances.
            """
        ),
        from_sql=EnumMapUtils.from_sql_named_fields(
            {
                "holy_res": "Holy", 
                "fire_res": "Fire", 
                "nature_res": "Nature", 
                "frost_res": "Frost",
                "shadow_res": "Shadow",
                "arcane_res": "Arcane",
            },
        ),
    )
    scalingStatDistribution: int = Field(
        default=0,
        description=dedent(
            """
            Similar to Static Stats these are the Stats that grow along with the
            users level (mainly heirloom leveling gear) use like static stats.
            """
        ),
        from_sql=direct_map("ScalingStatDistribution"),
    )
    scalingStatValue: int = Field(
        default=0,
        description=dedent(
            """
            Final (level 80) value of the scaling-stat
            """
        ),
        from_sql=direct_map("ScalingStatValue"),
    )
    stats: dict[(ItemStat | int), int] = Field(
        # TODO: must include `statCount` in serialization
        default=dict(),
        description=dedent(
            """
            Stats applied to the item in key-value pairs.
            """
        ),
        from_sql=EnumMapUtils.stats_from_sql_kvpairs(
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
    )
    sockets: ItemSockets = Field(
        default=ItemSockets(),
        description=dedent(
            """
            Item socket details.
            """
        ),
        from_sql=ItemSockets.from_sql(),
    )
    armor: int = Field(
        default=0,
        description=dedent(
            """
            The armor value of the item.
            """
        ),
        from_sql=direct_map("armor"),
    )
    armorDamageModifier: int = Field(
        default=0,
        description=dedent(
            """
            This field is not well understood.
            """
        ),
        from_sql=direct_map("ArmorDamageModifier"),
    )
    hitDelay: int = Field(
        default=0,
        description=dedent(
            """
            The time in milliseconds between successive hits.
            """
        ),
        from_sql=direct_map("delay"),
    )
    ammoType: (AmmoType | int) = Field(
        default=AmmoType.Undefined,
        description=dedent(
            """
            The type of ammunition the item uses.
            """
        ),
        from_sql=EnumUtils.from_sql("ammo_type"),
    )
    weaponRange: int = Field(
        default=0,
        description=dedent(
            """
            The range modifier for bows, crossbows, and guns.
            All of Blizzard's ranged weapons have a default range of 100.
            """
        ),
        from_sql=direct_map("RangedModRange"),
    )
    block: int = Field(
        default=0,
        description=dedent(
            """
            If the item is a shield, this value will be the block chance of the
            shield.
            """
        ),
        from_sql=direct_map("block"),
    )
    durability: int = Field(
        default=100,
        description=dedent(
            """
            The durability of the item. Defaults to 100.
            """
        ),
        from_sql=direct_map("MaxDurability"),
    )
    sheath: (Sheath | int) = Field(
        default=Sheath.Undefined,
        description=dedent(
            """
            Controls how the item is put away on the character. Press the 'Z'
            hotkey to sheath and unsheathe your weapons.
            """
        ),
        from_sql=EnumUtils.from_sql("sheath"),
    )
    damage: Damage = Field(
        default=Damage(),
        description=dedent(
            """
            The damage values of the weapon.
            """
        ),
        from_sql=Damage.from_sql(),
    )
    spells: list[ItemSpell] = Field(
        default=[],
        description=dedent(
            """
            Items can be used to invoke spells.
            """
        ),
        # sql_fields=[
        #     "spellid_1",
        #     "spelltrigger_1",
        #     "spellcharges_1",
        #     "spellppmRate_1",
        #     "spellcooldown_1",
        #     "spellcategory_1",
        #     "spellcategorycooldown_1",
        #     "spellid_2",
        #     "spelltrigger_2",
        #     "spellcharges_2",
        #     "spellppmRate_2",
        #     "spellcooldown_2",
        #     "spellcategory_2",
        #     "spellcategorycooldown_2",
        #     "spellid_3",
        #     "spelltrigger_3",
        #     "spellcharges_3",
        #     "spellppmRate_3",
        #     "spellcooldown_3",
        #     "spellcategory_3",
        #     "spellcategorycooldown_3",
        #     "spellid_4",
        #     "spelltrigger_4",
        #     "spellcharges_4",
        #     "spellppmRate_4",
        #     "spellcooldown_4",
        #     "spellcategory_4",
        #     "spellcategorycooldown_4",
        #     "spellid_5",
        #     "spelltrigger_5",
        #     "spellcharges_5",
        #     "spellppmRate_5",
        #     "spellcooldown_5",
        #     "spellcategory_5",
        #     "spellcategorycooldown_5",
        # ],
    )
    build: int = Field(
        default=0,
        description="Indicates the build version that the item was added in.",
        from_sql=direct_map("VerifiedBuild"),
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
        assert(len(entity) == 1)

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
        return Item(**item_args)