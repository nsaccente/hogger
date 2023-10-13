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

import mysql.connector as db
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


def direct_map(sql_field: str):
    def direct_map(sql: dict[str, any]) -> any:
        return sql[sql_field]
    return direct_map 


class Item(Entity):
    type: Literal["Item"]
    # MISCELLANEOUS
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
        from_sql=direct_map("class"),
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
        from_sql=direct_map("Quality"),
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
        from_sql=direct_map("BuyPrice"),
    )
    # # buyPriceExtra
    sellPrice: Money = Field(
        default=Money(gold=0, silver=0, copper=0),
        description=dedent(
            """
            The amount a vendor will purchase this item from you for.
            """
        ),
        from_sql=direct_map("SellPrice"),
    )
    inventoryType: (InventoryType | int) = Field(
        default=InventoryType.NoEquip,
        description=dedent(
            """
            Is the item equippable? A quest item?
            """
        ),
        from_sql=direct_map("InventoryType"),
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
        from_sql=direct_map("BagFamily"),
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
        from_sql=direct_map("TotemCategory"),
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
        from_sql=direct_map("FoodType"),
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
        # from_sql=
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
        # from_sql=direct_map("MaxMoneyLoot"),
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
        from_sql=direct_map("bonding"),
    )

    # # FLAGS
    flags: list[ItemFlag | int] = Field(
        default=[],
        description=dedent(
            """
            A collection of flags to modify the behavior of the item.
            """
        ),
        from_sql=direct_map("Flags"),
    )
    flagsExtra: list[ItemFlagExtra | int] = Field(
        default=[],
        description=dedent(
            """
            A collection of flags to modify the behavior of the item.
            """
        ),
        # serialization_alias="FlagsExtra",
        sql_fields=["FlagsExtra"],
    )
    flagsCustom: list[ItemFlagExtra | int] = Field(
        default=[],
        description=dedent(
            """
            A collection of flags to modify the behavior of the item.
            """
        ),
        # serialization_alias="flagsCustom",
        sql_fields=["flagsCustom"],
    )

    # # TEXTS
    readText: ItemText = Field(
        default=ItemText(),
        sql_fields=["PageText", "PageMaterial", "LanguageID"],
    )

    # # REQUIREMENTS
    requires: Requires = Field(
        default=Requires(),
        description="",
        sql_fields=["PageText", "PageMaterial", "LanguageID"],

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
        # serialization_alias="ItemLevel",
        sql_fields=["ItemLevel"],
        ge=0,
    )
    unlocks: LookupID = Field(
        default=0,
        description=dedent(
            """
            The lock entry ID that this item (which serves as a key) is tied to.
            This field is used in key-door mechanics.
            """
        ),
        # serialization_alias="lockid",
        sql_fields=["lockid"],
    )

    # RESISTANCE
    resistances: dict[(ItemResistance | int), int] = Field(
        default=dict(),
        description=dedent(
            """
            Item resistances.
            """
        ),
        sql_fields={
            "Holy": "holy_res", 
            "Fire": "fire_res", 
            "Nature": "nature_res", 
            "Frost": "frost_res",
            "Shadow": "shadow_res",
            "Arcane": "arcane_res",
        },
    )

    # STATS
    scalingStatDistribution: int = Field(
        default=0,
        description=dedent(
            """
            Similar to Static Stats these are the Stats that grow along with the
            users level (mainly heirloom leveling gear) use like static stats.
            """
        ),
        # serialization_alias="ScalingStatDistribution",
        sql_fields=["ScalingStatDistribution"],
    )
    scalingStatValue: int = Field(
        default=0,
        description=dedent(
            """
            Final (level 80) value of the scaling-stat
            """
        ),
        # serialization_alias="ScalingStatValue",
        sql_fields=["ScalingStatValue"],
    )
    # TODO: We need to fill this back in when serialized.
    # statCount: int = Field(
    #     default=0,
    #     description=dedent(
    #         """
    #         The total number of stats attached to this item. Defaults to 0.
    #         """
    #     ),
    #     ge=0,
    #     # serialization_alias="StatsCount",
    #     sql_fields=["StatsCount"],
    # )
    stats: dict[(ItemStat | int), int] = Field(
        default=dict(),
        description=dedent(
            """
            Stats applied to the item in key-value pairs.
            """
        ),
        sql_fields=[
            "StatsCount",
            "stat_type1",
            "stat_value1",
            "stat_type2",
            "stat_value2",
            "stat_type3",
            "stat_value4",
            "stat_type5",
            "stat_value5",
            "stat_type6",
            "stat_value6",
            "stat_type7",
            "stat_value7",
            "stat_type8",
            "stat_value8",
            "stat_type9",
            "stat_value9",
            "stat_type10",
            "stat_value10",
        ],
    )

    # # SOCKETS
    sockets: ItemSockets = Field(
        default=ItemSockets(),
        description=dedent(
            """
            Item socket details.
            """
        ),
        sql_fields=[
            "GemProperties",
            "socketBonus",
            "socketColor_1",
            "socketColor_2",
            "socketColor_3",
            "socketContent_1",
            "socketContent_2",
            "socketContent_3",
        ],
    )

    # # WEAPON ARMOR
    armor: int = Field(
        default=0,
        description=dedent(
            """
            The armor value of the item.
            """
        ),
        # serialization_alias="armor",
        sql_fields=["armor"],
    )
    armorDamageModifier: int = Field(
        default=0,
        description=dedent(
            """
            This field is not well understood.
            """
        ),
        # serialization_alias="ArmorDamageModifier",
        sql_fields=["ArmorDamageModifier"],
    )
    hitDelay: int = Field(
        default=0,
        description=dedent(
            """
            The time in milliseconds between successive hits.
            """
        ),
        # serialization_alias="delay",
        sql_fields=["delay"],
        ge=0,
    )
    ammoType: (AmmoType | int) = Field(
        default=AmmoType.Undefined,
        description=dedent(
            """
            The type of ammunition the item uses.
            """
        ),
        # serialization_alias="ammo_type",
        sql_fields=["ammo_type"],
    )
    weaponRange: int = Field(
        default=0,
        description=dedent(
            """
            The range modifier for bows, crossbows, and guns.
            All of Blizzard's ranged weapons have a default range of 100.
            """
        ),
        # serialization_alias="RangedModRange",
        sql_fields=["RangedModRange"],
        ge=0,
    )
    block: int = Field(
        default=0,
        description=dedent(
            """
            If the item is a shield, this value will be the block chance of the
            shield.
            """
        ),
        # serialization_alias="block",
        sql_fields=["block"],
    )
    durability: int = Field(
        default=100,
        description=dedent(
            """
            The durability of the item. Defaults to 100.
            """
        ),
        # serialization_alias="MaxDurability",
        sql_fields=["MaxDurability"],
        ge=0,
    )
    sheath: (Sheath | int) = Field(
        default=Sheath.Undefined,
        description=dedent(
            """
            Controls how the item is put away on the character. Press the 'Z'
            hotkey to sheath and unsheathe your weapons.
            """
        ),
        # serialization_alias="sheath"
        sql_fields=["sheath"],
    )
    damage: Damage = Field(
        default=Damage(),
        description=dedent(
            """
            The damage values of the weapon.
            """
        ),
        sql_fields=["damage"],
    )

    # # SPELL
    spells: list[ItemSpell] = Field(
        default=[],
        description=dedent(
            """
            Items can be used to invoke spells.
            """
        ),
        sql_fields=[
            "spellid_1",
            "spelltrigger_1",
            "spellcharges_1",
            "spellppmRate_1",
            "spellcooldown_1",
            "spellcategory_1",
            "spellcategorycooldown_1",
            "spellid_2",
            "spelltrigger_2",
            "spellcharges_2",
            "spellppmRate_2",
            "spellcooldown_2",
            "spellcategory_2",
            "spellcategorycooldown_2",
            "spellid_3",
            "spelltrigger_3",
            "spellcharges_3",
            "spellppmRate_3",
            "spellcooldown_3",
            "spellcategory_3",
            "spellcategorycooldown_3",
            "spellid_4",
            "spelltrigger_4",
            "spellcharges_4",
            "spellppmRate_4",
            "spellcooldown_4",
            "spellcategory_4",
            "spellcategorycooldown_4",
            "spellid_5",
            "spelltrigger_5",
            "spellcharges_5",
            "spellppmRate_5",
            "spellcooldown_5",
            "spellcategory_5",
            "spellcategorycooldown_5",
        ],
    )
    build: int = Field(
        default=0,
        description="Indicates the build version that the item was added in.",
        # serialization_alias="VerifiedBuild",
        sql_fields=["VerifiedBuild"],
        ge=0,
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

        sql = dict(zip(cursor.column_names, entity[0]))
        for field, field_properties in Item.model_fields.items():
            json_schema_extra = field_properties.json_schema_extra
            if json_schema_extra is not None and "from_sql" in json_schema_extra:
                from_sql_func = json_schema_extra["from_sql"]
                result = from_sql_func(sql)
                print(field, result, type(result))

        print()
        print()
        print()
        print()
        return sql


    
    @staticmethod
    def from_sql(sql: dict[str, any]) -> "Item":
        f = Item.model_fields["id"].json_schema_extra["from_sql"]
        print(f(sql))

        # for field_name, field_properties in list(Item.model_fields.items())[0:15]:
        #     try:
        #         sql_fields = field_properties.json_schema_extra["from_sql"]
        #     except:
        #         sql_fields = None
            
        #     if sql_fields is not None:
        #         anno = field_properties.annotation
        #         print(field_name, sql_fields, anno)
                # if issubclass(IntFlag, anno):
                #     print(anno)
                # if issubclass(Enum, anno):
                #     print(anno)



        # item_fields = {
        #     "name": sql.pop("name"),
        #     # "itemSubclass": sql.pop("")
        # }
        # for sql_field, model_field in _sql_to_model.items():
        #     item_fields[model_field] = sql.pop(sql_field)

        # # Stats
        # item_fields["stats"] = {}
        # for i in range(1, 11):
        #     stat_type = sql.pop(f"stat_type{i}")
        #     stat_value = sql.pop(f"stat_value{i}")
        #     item_fields["stats"][ItemStat(stat_type)] = stat_value
        
        # # Damage
        # item_fields["damage"] = {
        #     "min1": sql.pop("dmg_min1"),
        #     "max1": sql.pop("dmg_max1"),
        #     "type1": sql.pop("dmg_type1"),
        #     "min2": sql.pop("dmg_min2"),
        #     "max2": sql.pop("dmg_max2"),
        #     "type2": sql.pop("dmg_type2"),
        # }

        # # Spells 
        # item_fields["spells"] = []
        # for i in range(1, 6):
        #     item_fields["spells"].append(
        #         {
        #             "id": sql.pop(f"spellid_{i}"),
        #             "trigger": sql.pop(f"spelltrigger_{i}"),
        #             "charges": sql.pop(f"spellcharges_{i}"),
        #             "procsPerMinute": sql.pop(f"spellppmRate_{i}"),
        #             "cooldown": sql.pop(f"spellcooldown_{i}"),
        #             "category": sql.pop(f"spellcategory_{i}"),
        #             "cooldownCategory": sql.pop(f"spellcategorycooldown_{i}"),
        #         }
        #     )
            
        # # Resistances 
        # item_fields["resistances"] = {}
        # for resistance in ItemResistance:
        #     res = f"{resistance.name.lower()}_res"
        #     item_fields["resistances"][resistance] = sql.pop(res)

        # # ItemText
        # item_fields["readText"] = {
        #     "id": sql.pop("PageText"),
        #     "pageMaterial": sql.pop("PageMaterial"),
        #     "language": sql.pop("LanguageID"),
        # }
        
        # # Gems
        # gems = {1: 0, 2: 0, 4: 0, 8: 0}
        # for i in range(1, 4):
        #     color = sql.pop(f"socketColor_{i}")
        #     count = sql.pop(f"socketContent_{i}")
        #     if color not in gems:
        #         gems[color] = 0
        #     gems[color] += count
        # item_fields["sockets"] = {
        #     "socketBonus": sql.pop("socketBonus"),
        #     "properties": sql.pop("GemProperties"),
        #     "meta": gems[1],
        #     "red": gems[2],
        #     "yellow": gems[4],
        #     "blue": gems[8],
        # }

        # # randomStat
        # item_fields["randomStat"] = {
        #     "id": max(sql.pop("RandomProperty"), sql["RandomSuffix"]),
        #     "randomSuffix": sql.pop("RandomSuffix"),
        # }

        # for k, v in sql.items():
        #     print(k, v)
        # return Item(**item_fields)
            