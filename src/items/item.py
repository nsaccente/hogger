import abc
import typing

from pydantic import (BaseModel, Field, FieldValidationInfo, SerializationInfo,
                      field_serializer, field_validator)

from src.misc import Duration, Money

from .item_enums import *
from .item_flags import *


class Item(BaseModel, abc.ABC):
    class Config:
        sql: bool = True
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
    startsQuest: int = Field(
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
    itemLimitCategory: int = Field(
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
    # flags: ItemFlags = Field(
    #     default=ItemFlags(),
    #     description=("A collection of flags to modify the behavior of the item."),
    # )

    # TEXTS
    # pageText
    # pageMaterial
    # LanguageID

    # REQUIREMENTS

    @field_validator(
        "bonding",
        "foodType", 
        "inventoryType", 
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
        "material", 
        "quality", 
        "totemCategory", 
        when_used="json-unless-none",
    )
    def serialize_enum(self, v: Enum, info: SerializationInfo) -> str:
        return v.name

    @field_validator(
            "bagFamily", 
            mode="before",
    )
    def parse_intflag(cls, items: list[str | int], info: FieldValidationInfo) -> list[IntFlag | int]:
        intflag_type = (
            list(
                filter(
                    lambda field_type: (issubclass(field_type, IntFlag)),
                    (
                        typing.get_type_hints(cls)[info.field_name]
                        .__args__[0] # args passed to list[]
                        .__args__ # args passed to Union[]
                    ),
                )
            ) # convert the elements returned by filter to a list
            [0] # grab the first element in the list.
        )

        intflag_max = [i.value for i in intflag_type]
        result = []
        for item in items:
            if isinstance(item, str):
                print(f"STRING{item}")
                try:
                    result.append(intflag_type[item])
                except:
                    raise Exception(
                        f'"{item}" not a valid value for "{intflag_type.__name__}'
                    )
            elif isinstance(item, int):
                flag = 2**item
                if flag in intflag_max:
                    result.append(intflag_type(int(2**item)))
                else:
                    result.append(int(item))
            elif issubclass(IntFlag, item):
                result.append(item)
            
        return result


    # @field_serializer(
    #     "bagFamily", 
    #     # "flags",
    #     when_used="json-unless-none",
    # )
    # def serialize_bitmask(self, bitmask: , info: SerializationInfo) -> list[str]:
    #     items = []
    #     for key, value in vars(bitmask).items():
    #         if value:
    #             items.append(key)
    #     int(bitmask)
    #     return items

