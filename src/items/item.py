import abc

from pydantic import BaseModel, Field, FieldValidationInfo, field_validator

from src.misc import Money, Time

from .item_properties import *


class Item(BaseModel, abc.ABC):
    name: str = Field(
        description="The name of the item",
    )
    description: str = Field(
        default="",
        description=(
            "The description that appears in yellow letters at the bottom of "
            "the item tooltip"
        ),
    )
    scriptName: str = Field(
        default="",
        description="The name of the script that the item should use",
    )
    soundOverride: int = Field(
        default=-1,
        description=(
            "Each weapon type plays a unique sound on impact, which can be "
            "overriden by the unique sound of a different weapon type"
        ),
    )
    displayId: int = Field(
        description="Controls both the model appearance and icon.",
    )
    quality: Quality = Field(
        default=Quality.Common,
        description=(
            "The quality of the item; valid values are: Poor, Uncommon, "
            "Common, Rare, Epic, Legendary, Artifact, BoA"
        ),
    )
    buyCount: int = Field(
        default=1,
        description=(
            "The size of the item stack when sold by vendors. If a vendor has "
            "a limited number of this item available, the vendor's inventory "
            "will increase by this number when the vendor list is refreshed "
            "(see npc.vendor.incrtime)."
        ),
    )
    buyPrice: Money = Field(
        default=Money(gold=0, silver=0, copper=0),
        description="The cost to purchase this item form a vendor",
    )
    sellPrice: Money = Field(
        default=Money(gold=0, silver=0, copper=0),
        description="The amount a vendor will purchase this item from you for",
    )
    inventoryType: InventoryType = Field(
        default=InventoryType.NoEquip,
        description="Is the item equippable? A quest item?",
    )
    maxAmount: int = Field(
        default=1,
        description="The maximum amount that a player can have; use 0 for infinite",
    )
    stackSize: int = Field(
        default=1,
        description="The maximum size of a stack of this item.",
    )
    startsQuest: int = Field(
        default=0,
        description=(
            "The ID of the quest that this item will start if right-clicked. "
            "See quest_template.id"
        ),
    )
    material: Material = Field(
        default=Material.Undefined,
        description="Controls the sound played when moving items in your inventory",
    )
    bagFamily: BagFamily = Field(
        default=BagFamily(),
        description="Dictates what kind of bags this item can be placed in.",
    )
    # randomItemProperty
    # randomPropertyItem with RandomProperty = 863
    # Item with RandomSuffix = 24585
    # min(RandomProperty, RandomSuffix) must equal 0.
    containerSlots: int = Field(
        default=0,
        description=(
            "If this item is a bag, controls the number of slots it will have"
        ),
    )
    specialUse: TotemCategory = Field(
        default=TotemCategory.Undefined,
        description=(
            "Some items are required to complete certain tasks, such as a "
            "shaman's totems, "
        ),
    )
    duration: Time = Field(
        default=Time(),
        description=(
            "The amount of time an item will exist in a player's inventory "
            "before disappearing; setting the duration to 0 seconds will "
            "prevent the item from every disappearing"
        ),
    )
    itemLimitCategory: int = Field(
        default=0,
        description=(
            'defines if an item belongs to a "category", like "Mana Gems" or '
            'Healthstone" and it defines how many items of the category you '
            'can have in the bag (this is the "limit"). For example, for '
            'Healthstone, there are several items like "Lesser Healthstone, '
            'Greater Healthstone, etc." but you can have only one in your bag '
            "(check as example value 3 or 4)."
        ),
    )
    # disenchantId = <SELECT * FROM `item_template` WHERE `itemLimitCategory`>

    @field_validator("buyCount", "stackSize")
    def integer_greater_than_zero(cls, v: int, info: FieldValidationInfo) -> int:
        if v <= 0:
            raise Exception("Value for {} must be non-negative".format(info.field_name))
        return v

    @field_validator("displayId", "maxAmount")
    def non_negative_integer(cls, v: int, info: FieldValidationInfo) -> int:
        if v < 0:
            raise Exception("Value for {} must be non-negative".format(info.field_name))
        return v

    @field_validator("buyPrice", "sellPrice", mode="after")
    def prevent_negative_money(cls, v: Money, info: FieldValidationInfo) -> Money:
        if (v.gold < 0) or (v.silver < 0) or (v.copper < 0):
            raise Exception(
                "Money amount cannot be negative for {}".format(info.field_name)
            )
        return v

    @field_validator("inventoryType", mode="before")
    def parse_inventory_type(cls, v: str, info: FieldValidationInfo) -> InventoryType:
        try:
            return InventoryType[v]
        except:
            raise Exception('"{}" is an invalid value for inventoryType'.format(v))

    @field_validator("quality", mode="before")
    def parse_quality(cls, v: str, info: FieldValidationInfo) -> Quality:
        try:
            return Quality[v]
        except:
            raise Exception('"{}" is an invalid value for quality'.format(v))

    @field_validator("bagFamily", mode="before")
    def parse_bag_family(cls, v: list[str], info: FieldValidationInfo) -> BagFamily:
        bag_families = vars(BagFamily)["__annotations__"].keys()
        bf = BagFamily()
        for item in v:
            if not item in bag_families:
                raise Exception("{} not a valid value for bagFamily".format(v))
            bf[item] = True
        return bf
