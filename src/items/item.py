import abc

from pydantic import BaseModel, Field, FieldValidationInfo, field_validator, field_serializer, SerializationInfo

from src.misc import Money, Duration

from .item_properties import *


class Item(BaseModel, abc.ABC):
    # MISCELLANEOUS
    id: int = Field(
        default=-1,
        description=
        (
            "Identifier for the item in the world database. Set to -1 to "
            "automagically use the first item id it finds. Default is -1."
        ),
        serialization_alias="entry",
    )
    id_offset: int = Field(
        default=60000,
        description=(
            "Dictates the first id the item is allowed to use. This allows "
            "separation of custom items and vanilla items."
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
            "The description that appears in yellow letters at the bottom of "
            "the item tooltip. No description by default."
        ),
    )
    scriptName: str = Field(
        default="",
        description=(
            "The name of the script that the item should use. No script by "
            "default."
        ),
        serialization_alias="ScriptName",
    )
    itemClass: ItemClass = Field(
        default=ItemClass.TradeGoods,
        description=(
            "The category the item belongs to; e.g. consumable, weapon, "
            "armor, etc."
        ),
        serialization_alias="class",
    )
    itemSubclass: int = Field(
        defalt=0,
        description=(
            "The subcategory the item belongs to, and is dependent upon the "
            "value of itemClass."
        ),
        serialization_alias="subclass",
    )
    soundOverride: int = Field(
        default=-1,
        description=(
            "Each weapon type plays a unique sound on impact, which can be "
            "overriden by the unique sound of a different weapon type. "
            "Use -1 to use the default sound for the item. Default is -1."
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
            "The quality of the item; valid values are: Poor, Uncommon, "
            "Common, Rare, Epic, Legendary, Artifact, BoA"
        ),
        serialization_alias="Quality",
    )
    buyCount: int = Field(
        default=1,
        description=(
            "The size of the item stack when sold by vendors. If a vendor has "
            "a limited number of this item available, the vendor's inventory "
            "will increase by this number when the vendor list is refreshed "
            "(see npc.vendor.incrtime)."
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
            "The ID of the quest that this item will start if right-clicked. "
            "See quest_template.id"
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
        default = 0,
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
    bagFamily: BagFamily = Field(
        default=BagFamily(),
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
            "Some items are required to complete certain tasks, such as a "
            "shaman's totems, "
        ),
        serialization_alias="TotemCategory",
    )
    duration: Duration = Field(
        default=Duration(),
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
        serialization_alias="ItemLimitCategory",
    )
    # TODO: Create dedicated DisenchantID Class
    disenchantId: int = Field(
        default=0,
        description="Corresponds to an entry in disenchant_loot_template.",
        serialization_alias="DisenchantID",
    )


    @field_validator("inventoryType", mode="before")
    def parse_inventory_type(cls, v: str, info: FieldValidationInfo) -> InventoryType:
        print(info)
        try:
            return InventoryType[v]
        except:
            raise Exception(f'"{v}" is an invalid value for inventoryType')

    @field_validator("quality", mode="before")
    def parse_quality(cls, v: str, info: FieldValidationInfo) -> Quality:
        try:
            return Quality[v]
        except:
            raise Exception(f'"{v}" is an invalid value for quality')

    @field_validator("bagFamily", mode="before")
    def parse_bag_family(cls, v: list[str], info: FieldValidationInfo) -> BagFamily:
        bag_families = vars(BagFamily)["__annotations__"].keys()
        bf = BagFamily()
        for item in v:
            if not item in bag_families:
                raise Exception(f'"{v}" not a valid value for bagFamily')
            bf[item] = True
        return bf

    @field_serializer("inventoryType", "material", "quality", "totemCategory")
    def serialize_enum(self, v: Enum, _info: SerializationInfo) -> str:
        return v.name

    @field_serializer("bagFamily")
    def serialize_bag_family(self, bf: BagFamily, _info: SerializationInfo) -> list[str]:
        families = []
        for family, value in vars(bf).items():
            if value:
                families.append(family)
        print(families)

        return families
