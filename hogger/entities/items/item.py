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
from hogger.misc import *

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
    "requiredHonorRank",
    "requiredReputationRank",
    "sheath",
    "totemCategory",
]

_intflag_fields = [
    "bagFamily",
    "classes",
    "flags",
    "flagsCustom",
    "flagsExtra",
    "races",
]

_enum_map_fields = [
    "resistances",
    "stats",
]

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
        serialization_alias="entry",
    )
    name: str = Field(
        description=dedent(
            """
            The name of the item.
            """
        ),
        serialization_alias="name",
    )
    description: str = Field(
        default="",
        description=dedent(
            """
            The description that appears in yellow letters at the bottom of
            the item tooltip. No description by default.
            """
        ),
        serialization_alias="description",
    )
    scriptName: str = Field(
        default="",
        description=dedent(
            """
            The name of the script that the item should use. No script by
            default.
            """
        ),
        serialization_alias="ScriptName",
    )
    itemClass: (ItemClass | int) = Field(
        default=ItemClass.TradeGoods,
        description=dedent(
            """
            The category the item belongs to; e.g. consumable, weapon, armor,
            etc.
            """
        ),
        serialization_alias="class",
    )
    itemSubclass: int = Field(
        defalt=0,
        description=dedent(
            """
            The subcategory the item belongs to, and is dependent upon the
            value of itemClass.
            """
        ),
        serialization_alias="subclass",
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
        serialization_alias="SoundOverrideSubclass",
        ge=-1,
    )
    displayId: int = Field(
        default=0,
        description=dedent(
            """
            Controls both the model appearance and icon.
            """
        ),
        serialization_alias="displayid",
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
        serialization_alias="Quality",
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
        serialization_alias="BuyCount",
        ge=1,
    )
    buyPrice: Money = Field(
        default=Money(gold=0, silver=0, copper=0),
        description=dedent(
            """
            The cost to purchase this item form a vendor
            """
        ),
        serialization_alias="BuyPrice",
    )
    # # buyPriceExtra
    sellPrice: Money = Field(
        default=Money(gold=0, silver=0, copper=0),
        description=dedent(
            """
            The amount a vendor will purchase this item from you for.
            """
        ),
        serialization_alias="SellPrice",
    )
    inventoryType: (InventoryType | int) = Field(
        default=InventoryType.NoEquip,
        description=dedent(
            """
            Is the item equippable? A quest item?
            """
        ),
        serialization_alias="InventoryType",
    )
    maxCount: int = Field(
        default=1,
        description=dedent(
            """
            The maximum amount that a player can have; use 0 for infinite.
            """
        ),
        serialization_alias="maxcount",
        ge=0,
    )
    stackSize: int = Field(
        default=1,
        description=dedent(
            """
            The maximum size of a stack of this item.
            """
        ),
        serialization_alias="stackable",
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
        serialization_alias="startquest",
    )
    material: (Material | int) = Field(
        default=Material.Undefined,
        description=dedent(
            """
            Controls the sound played when moving items in your inventory.
            """
        ),
        serialization_alias="Material",
    )
    randomStat: RandomStat = Field(
        default=RandomStat(),
        description=dedent(
            """
            Adds a random stat bonus on the item.
            """
        ),
    )
    bagFamily: list[BagFamily | int] = Field(
        default=[],
        description=dedent(
            """
            Dictates what kind of bags this item can be placed in.
            """
        ),
        serialization_alias="BagFamily",
    )
    containerSlots: int = Field(
        default=0,
        description=dedent(
            """
            If this item is a bag, controls the number of slots it will have
            """
        ),
        serialization_alias="ContainerSlots",
    )
    totemCategory: (TotemCategory | int) = Field(
        default=TotemCategory.Undefined,
        description=dedent(
            """
            Some items are required to complete certain tasks, such as a
            shaman's totems, blacksmithing hammers, or enchanting rods.
            """
        ),
        serialization_alias="TotemCategory",
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
        serialization_alias="duration",
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
        serialization_alias="ItemLimitCategory",
    )
    disenchantId: LookupID = Field(
        default=0,
        description=dedent(
            """
            Corresponds to an entry in disenchant_loot_template.
            """
        ),
        serialization_alias="DisenchantID",
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
        serialization_alias="FoodType",
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
        serialization_alias="minMoneyLoot",
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
        serialization_alias="maxMoneyLoot",
    )
    itemSet: LookupID = Field(
        default=0,
        description=dedent(
            """
            The ID of the item set that this item belongs to.
            """
        ),
        ge=0,
        serialization_alias="itemset",
    )
    bonding: (ItemBinding | int) = Field(
        default=ItemBinding.Never,
        description=dedent(
            """
            Determines if the item binds to the character. Defaults to Never.
            """
        ),
        serialization_alias="bonding",
    )

    # # FLAGS
    flags: list[ItemFlag | int] = Field(
        default=[],
        description=dedent(
            """
            A collection of flags to modify the behavior of the item.
            """
        ),
        serialization_alias="Flags",
    )
    flagsExtra: list[ItemFlagExtra | int] = Field(
        default=[],
        description=dedent(
            """
            A collection of flags to modify the behavior of the item.
            """
        ),
        serialization_alias="FlagsExtra",
    )
    flagsCustom: list[ItemFlagExtra | int] = Field(
        default=[],
        description=dedent(
            """
            A collection of flags to modify the behavior of the item.
            """
        ),
        serialization_alias="flagsCustom",
    )

    # # TEXTS
    text: ItemText = Field(
        default=ItemText(),
    )

    # # REQUIREMENTS
    classes: list[AllowableClass | int] = Field(
        default=[],
        description=dedent(
            """
            Classes permitted to use the item.
            """
        ),
        serialization_alias="AllowableClass",
    )
    races: list[AllowableRace | int] = Field(
        default=[],
        description=dedent(
            """
            Races permitted to use the item.
            """
        ),
        serialization_alias="AllowableRace",
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
        serialization_alias="ItemLevel",
        ge=0,
    )
    requiredLevel: int = Field(
        default=1,
        descrption=dedent(
            """
            The minimum player level required to equip the item.
            """
        ),
        serialization_alias="RequiredLevel",
        ge=1,
    )
    requiredSkill: LookupID = Field(
        default=0,
        description=dedent(
            """
            The skill required to use this item.
            """
        ),
        serialization_alias="RequiredSkill",
        ge=0,
    )
    requiredSkillRank: int = Field(
        default=0,
        description=dedent(
            """
            The required skill rank the player needs to have to use this item.
            """
        ),
        serialization_alias="RequiredSkillRank",
    )
    requiredSpell: LookupID = Field(
        default=0,
        description=dedent(
            """
            The required spell that the player needs to have to use this item.
            """
        ),
        serialization_alias="requiredspell",
    )
    requiredHonorRank: (RequiredHonorRank | int) = Field(
        default=RequiredHonorRank.Undefined,
        description=dedent(
            """
            The required PvP rank required to use the item.",
            serialization_alias="requiredhonorrank",
            """
        ),
        serialization_alias="requiredhonorrank",
    )
    requiredCityRank: int = Field(
        default=0,
        description=dedent(
            """
            Unused. All items have this set to 0.
            """
        ),
        serialization_alias="RequiredCityRank",
        ge=0,
    )
    requiredReputationFaction: int = Field(
        default=0,
        description=dedent(
            """
            The faction template ID of the faction that the player has to have
            a certain ranking with. If this value is 0, the faction of the
            seller of the item is used.
            """
        ),
        serialization_alias="RequiredReputationFaction",
        ge=0,
    )
    requiredReputationRank: (ReputationRank | int) = Field(
        default=0,
        description=dedent(
            """
            The required reputation rank to use the item.
            """
        ),
        serialization_alias="RequiredReputationRank",
        ge=0,
    )
    requiredDisenchantSkill: int = Field(
        default=0,
        description=dedent(
            """
            The required skill proficiency in disenchanting that the player must
            have in order to disenchant this item.
            """
        ),
        serialization_alias="RequiredDisenchantSkill",
        ge=0,
    )
    requiredMap: LookupID = Field(
        default=0,
        description=dedent(
            """
            The ID of the map in which this item can be used. If you leave the
            map, the item will be deleted from the inventory.
            """
        ),
        serialization_alias="Map",
        ge=0,
    )
    requiredArea: LookupID = Field(
        default=0,
        description=dedent(
            """
            The ID of the zone in which this item can be used. If you leave the
            area, the item will be deleted from the inventory.
            """
        ),
        serialization_alias="area",
    )
    requiredHoliday: LookupID = Field(
        default=0,
        description=dedent(
            """
            The holiday event that must be active in order to use the item.
            """
        ),
        serialization_alias="HolidayId",
    )
    unlocks: LookupID = Field(
        default=0,
        description=dedent(
            """
            The lock entry ID that this item (which serves as a key) is tied to.
            This field is used in key-door mechanics.
            """
        ),
        serialization_alias="lockid",
    )

    # RESISTANCE
    resistances: dict[(ItemResistance | int), int] = Field(
        default=dict(),
        description=dedent(
            """
            Item resistances.
            """
        ),
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
        serialization_alias="ScalingStatDistribution",
    )
    scalingStatValue: int = Field(
        default=0,
        description=dedent(
            """
            Final (level 80) value of the scaling-stat
            """
        ),
        serialization_alias="ScalingStatValue",
    )
    statCount: int = Field(
        default=0,
        description=dedent(
            """
            The total number of stats attached to this item. Defaults to 0.
            """
        ),
        ge=0,
        exclude=True,
        serialization_alias="StatsCount",
    )
    stats: dict[(ItemStat | int), int] = Field(
        default=dict(),
        description=dedent(
            """
            Stats applied to the item in key-value pairs.
            """
        ),
    )

    # # SOCKETS
    sockets: ItemSockets = Field(
        default=ItemSockets(),
        description=dedent(
            """
            Item socket details.
            """
        ),
    )

    # # WEAPON ARMOR
    armor: int = Field(
        default=0,
        description=dedent(
            """
            The armor value of the item.
            """
        ),
        serialization_alias="armor",
    )
    armorDamageModifier: int = Field(
        default=0,
        description=dedent(
            """
            This field is not well understood.
            """
        ),
        serialization_alias="ArmorDamageModifier",
    )
    hitDelay: int = Field(
        default=0,
        description=dedent(
            """
            The time in milliseconds between successive hits.
            """
        ),
        serialization_alias="delay",
        ge=0,
    )
    ammoType: (AmmoType | int) = Field(
        default=AmmoType.Undefined,
        description=dedent(
            """
            The type of ammunition the item uses.
            """
        ),
        serialization_alias="ammo_type",
    )
    weaponRange: int = Field(
        default=0,
        description=dedent(
            """
            The range modifier for bows, crossbows, and guns.
            All of Blizzard's ranged weapons have a default range of 100.
            """
        ),
        serialization_alias="RangedModRange",
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
        serialization_alias="block",
    )
    durability: int = Field(
        default=100,
        description=dedent(
            """
            The durability of the item. Defaults to 100.
            """
        ),
        serialization_alias="MaxDurability",
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
        serialization_alias="sheath"
    )
    damage: Damage = Field(
        default=Damage(),
        description=dedent(
            """
            The damage values of the weapon.
            """
        ),
    )

    # # SPELL
    spells: list[ItemSpell] = Field(
        default=[],
        description=dedent(
            """
            Items can be used to invoke spells.
            """
        ),
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
        Item.from_sql(dict(zip(cursor.column_names, entity[0])))

        return None

    
    @staticmethod
    def from_sql(sql: dict[str, any]) -> "Item":
        item_fields = {}
        for sql_field, model_field in _sql_to_model.items():
            item_fields[model_field] = sql.pop(sql_field)

        item_fields["stats"] = {}
        for i in range(1, 11):
            stat_type = sql.pop(f"stat_type{i}")
            stat_value = sql.pop(f"stat_value{i}")
            item_fields["stats"][ItemStat(stat_type)] = stat_value
        
        # item_fields["damage"] = Damage(**sql)
        item_fields["damage"] = {
            "min1": sql.pop("dmg_min1"),
            "max1": sql.pop("dmg_max1"),
            "type1": sql.pop("dmg_type1"),
            "min2": sql.pop("dmg_min2"),
            "max2": sql.pop("dmg_max2"),
            "type2": sql.pop("dmg_type2"),
        }

        item_fields["spells"] = []
        for i in range(1, 6):
            item_fields["spells"].append(
                {
                    "id": sql.pop(f"spellid_{i}"),
                    "trigger": sql.pop(f"spelltrigger_{i}"),
                    "charges": sql.pop(f"spellcharges_{i}"),
                    "procsPerMinute": sql.pop(f"spellppmRate_{i}"),
                    "cooldown": sql.pop(f"spellcooldown_{i}"),
                    "category": sql.pop(f"spellcategory_{i}"),
                    "cooldownCategory": sql.pop(f"spellcategorycooldown_{i}"),
                }
            )
            
        

        print(len(sql))
        item_fields["resistances"] = {}
        for resistance in ItemResistance:
            res = f"{resistance.name.lower()}_res"
            item_fields["resistances"][res] = sql.pop(res)
        for k, v in sql.items():
            print(k, v)
            


# Construct a constant used to map sql fields to model fields AFTER the model
# has been defind above.
_sql_to_model: dict[str, str] = {}
for field, metadata in Item.model_fields.items():
    if metadata.serialization_alias is not None:
        _sql_to_model[metadata.serialization_alias] = field 
    