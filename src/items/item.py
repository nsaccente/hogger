import abc
import typing

from pydantic import (BaseModel, Field, FieldValidationInfo, SerializationInfo,
                      field_serializer, field_validator)

from src.misc import Duration, Money

from .item_enums import *
from .item_damage import *
from .item_flags import *
from .item_sockets import *
from src.misc.currency import LookupID



class Item(BaseModel, abc.ABC):
    # MISCELLANEOUS
    id: int = Field(
        default=-1,
        description=(
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
        description=(
            """
            Dictates the first id the item is allowed to use. This allows
            separation of custom items and vanilla items.
            """
        ),
        exclude=True,
        ge=0,
    )
    name: str = Field(
        description="The name of the item",
    )
    description: str = Field(
        default="",
        description=(
            """
            The description that appears in yellow letters at the bottom of
            the item tooltip. No description by default.
            """
        ),
    )
    scriptName: str = Field(
        default="",
        description=(
            """
            The name of the script that the item should use. No script by
            default.
            """
        ),
        serialization_alias="ScriptName",
    )
    itemClass: ItemClass = Field(
        default=ItemClass.TradeGoods,
        description=(
            """
            The category the item belongs to; e.g. consumable, weapon, armor,
            etc.
            """
        ),
        serialization_alias="class",
    )
    itemSubclass: int = Field(
        defalt=0,
        description=(
            """
            The subcategory the item belongs to, and is dependent upon the
            value of itemClass.
            """
        ),
        serialization_alias="subclass",
    )
    soundOverride: int = Field(
        default=-1,
        description=(
            """
            Each weapon type plays a unique sound on impact, which can be
            overriden by the unique sound of a different weapon type.
            Use -1 to use the default sound for the item. Default is -1.
            """
        ),
        serialization_alias="SoundOverride",
        ge=-1,
    )
    displayId: int = Field(
        default=0,
        description="Controls both the model appearance and icon.",
        serialization_alias="displayid",
        ge=0,
    )
    quality: Quality = Field(
        default=Quality.Common,
        description=(
            """
            The quality of the item; valid values are: Poor, Uncommon,
            Common, Rare, Epic, Legendary, Artifact, BoA.
            """
        ),
        serialization_alias="Quality",
    )
    buyCount: int = Field(
        default=1,
        description=(
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
        description="The cost to purchase this item form a vendor",
        serialization_alias="BuyPrice",
    )
    sellPrice: Money = Field(
        default=Money(gold=0, silver=0, copper=0),
        description="The amount a vendor will purchase this item from you for",
        serialization_alias="SellPrice",
    )
    inventoryType: InventoryType = Field(
        default=InventoryType.NoEquip,
        description="Is the item equippable? A quest item?",
        serialization_alias="InventoryType",
    )
    maxCount: int = Field(
        default=1,
        description="The maximum amount that a player can have; use 0 for infinite",
        serialization_alias="maxcount",
        ge=0,
    )
    stackSize: int = Field(
        default=1,
        description="The maximum size of a stack of this item.",
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
        description="Controls the sound played when moving items in your inventory",
        serialization_alias="Material",
    )
    # TODO: Create dedicated RandomProperty classes
    # Itemid with RandomProperty = 863
    randomProperty: int = Field(
        default=0,
        description="",
        serialization_alias="RandomProperty",
        ge=0,
    )
    # TODO: Create dedicated RandomSuffix classes
    # Itemid with RandomSuffix = 24585
    randomSuffix: int = Field(
        default=0,
        description="",
        serialization_alias="RandomSuffix",
        ge=0,
    )
    # min(RandomProperty, RandomSuffix) must equal 0.
    bagFamily: list[BagFamily | int] = Field(
        default=[],
        description="Dictates what kind of bags this item can be placed in.",
        serialization_alias="BagFamily",
    )
    containerSlots: int = Field(
        default=0,
        description=(
            "If this item is a bag, controls the number of slots it will have"
        ),
        serialization_alias="ContainerSlots",
    )
    totemCategory: TotemCategory = Field(
        default=TotemCategory.Undefined,
        description=(
            """
            Some items are required to complete certain tasks, such as a
            shaman's totems, blacksmithing hammers, or enchanting rods.
            """
        ),
        serialization_alias="TotemCategory",
    )
    duration: Duration = Field(
        default=Duration(),
        description=(
            """
            The amount of time an item will exist in a player's inventory
            before disappearing; setting the duration to 0 seconds will
            prevent the item from every disappearing.
            """
        ),
    )
    itemLimitCategory: LookupID = Field(
        default=0,
        description=(
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
    # TODO: Create dedicated DisenchantID Class
    disenchantId: int = Field(
        default=0,
        description="Corresponds to an entry in disenchant_loot_template.",
        serialization_alias="DisenchantID",
    )
    foodType: FoodType = Field(
        default=FoodType.Undefined,
        description=(
            """
            Determines the category a fooditem falls into, if any. This is
            primarily used to determine what items hunter pet's will eat.
            Defaults to "Undefined".
            """
        ),
        serialization_alias="FoodType",
    )
    minLootMoney: Money = Field(
        default=Money(),
        description=(
            """
            Minimum amount of money contained in the item. If an item should
            not contain money, use Money(gold=0, silver=0, copper=0), which
            is the default for this field.
            """
        ),
    )
    maxLootMoney: Money = Field(
        default=Money(),
        description=(
            """
            Max amount of money contained in the item. If an item should
            not contain money, use Money(gold=0, silver=0, copper=0), which
            is the default for this field.
            """
        ),
    )
    itemSet: int = Field(
        default=0,
        description=("The ID of the item set that this item belongs to."),
        ge=0,
        serialization_alias="itemset",
    )
    bonding: ItemBinding = Field(
        default=ItemBinding.Never,
        description=(
            "Determines if the item binds to the character. Defaults to Never."
        ),
    )

    # FLAGS
    flags: list[ItemFlag | int] = Field(
        default=[],
        description=("A collection of flags to modify the behavior of the item."),
    )
    flagsExtra: list[ItemFlagExtra | int] = Field(
        default=[],
        description=("A collection of flags to modify the behavior of the item."),
    )
    flagsCustom: list[ItemFlagExtra | int] = Field(
        default=[],
        description=("A collection of flags to modify the behavior of the item."),
    )

    # TEXTS
    pageText: LookupID = Field(
        default=0,
        description=(
            """
            The ID of the row in the `page_text` table corresponding to the text
            that will be shown to the player.
            """
        ),
        ge=0
    )
    pageMaterial: PageMaterial = Field(
        default=PageMaterial.Parchment,
        description=(
            """
            The material that the text will be displayed on to the player.
            Defaults to parchment.
            """
        ),
    )
    language: Language = Field(
        default=Language.Universal,
        description=(
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
        description="Classes permitted to use the item.",
        serialization_alias="AllowableClass",
    )
    races: list[AllowableRace | int] = Field(
        default=[],
        description="Races permitted to use the item.",
        serialization_alias="AllowableRace",
    )
    itemLevel: int = Field(
        # TODO: Add automatic item level calculation as default.
        default=0,
        description="""
            The level of the item, not to be confused with the item required to
            equip or use the item.
        """,
        serialization_alias="ItemLevel",
        ge=0,
    )
    requiredLevel: int = Field(
        default=1,
        descrption="The minimum player level required to equip the item.",
        serialization_alias="RequiredLevel",
        ge=1,
    )
    # requiredSkill: Lookup = Field(

    # )
    # requiredSkillRank:
    # RequiredSpell
    requiredHonorRank: RequiredHonorRank = Field(
        default=RequiredHonorRank.Undefined,
        description="The required PvP rank required to use the item.",
        serialization_alias="requiredhonorrank",
    )
    requiredCityRank: int = Field(
        default=0,
        description="Unused. All items have this set to 0.",
        serialization_alias="RequiredCityRank",
        ge=0,
    )
    # requiredRepFaction
    # RequiredRepRank
    disenchantSkill: int = Field(
        default=-1,
        description="""
        The required skill proficiency in disenchanting that the player must
        have in order to disenchant this item.
        """,
        serialization_alias="",
        ge=-1,
    )
    # map
    # area
    # requiredHoliday
    # lock_id

    # RESISTANCE
    resistances: dict[ItemResistance, int] = Field(
        default=dict(),
        description=(
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
        description=(
            """
            The total number of stats attached to this item. Defaults to 0.
            """
        ),
        ge=0,
    )
    stats: dict[ItemStat, int] = Field(
        default=dict(),
        description=(
            """
            Stats applied to the item in key-value pairs.
            """
        ),
    )

    # SOCKETS
    sockets: ItemSockets = Field(
        default=ItemSockets(),
        description=(
            """
            Item socket details.
            """
        ),
    )

    # WEAPON ARMOR
    armor: int = Field(
        default=0,
        description=(
            """
            The armor value of the item.
            """
        ),
    )
    armorDamageModifier: int = Field(
        default=0,
        description=(
            """
            This field is not well understood.
            """
        ),
    )
    hitDelay: int = Field(
        default=0,
        description=(
            """
            The time in milliseconds between successive hits.
            """
        ),
        ge=0,
    )
    ammoType: AmmoType = Field(
        default=AmmoType.Undefined,
        description=(
            """
            The type of ammunition the item uses.
            """
        ),
    )
    weaponRange: int = Field(
        default=0,
        description=(
            """
            The range modifier for bows, crossbows, and guns.
            All of Blizzard's ranged weapons have a default range of 100.
            """
        ),
        ge=0,
    )
    block: int = Field(
        default=0,
        description=(
            """
            If the item is a shield, this value will be the block chance of the
            shield.
            """
        ),
    )
    durability: int = Field(
        default=100,
        description=(
            """
            The durability of the item. Defaults to 100.
            """
        ),
    )
    damage: Damage = Field(
        default=Damage(),
        description="The damage values of the weapon.",
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
        when_used="json-unless-none",
    )
    def serialize_enum(self, v: Enum, info: SerializationInfo) -> str:
        return v.name

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
        when_used="json-unless-none",
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
        when_used="json-unless-none",
    )
    def serialize_enum_map(
        self, items: dict[Enum, int], info: SerializationInfo
    ) -> dict[str, int]:
        return {str(k.name): v for k, v in items.items()}
