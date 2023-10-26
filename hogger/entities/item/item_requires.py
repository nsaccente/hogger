from enum import IntFlag, auto, IntEnum
from textwrap import dedent

from mysql.connector.cursor_cext import CMySQLCursor as Cursor
from pydantic import BaseModel, Field

from hogger.types import IntFlagUtils, LookupID


class AllowableClass(IntFlag):
    Warrior: int = auto()
    Paladin: int = auto()
    Hunter: int = auto()
    Rogue: int = auto()
    Priest: int = auto()
    DeathKnight: int = auto()
    Shaman: int = auto()
    Mage: int = auto()
    Warlock: int = auto()
    UNUSED: int = auto()
    Druid: int = auto()


class AllowableRace(IntFlag):
    Human: int = auto()
    Orc: int = auto()
    Dwarf: int = auto()
    NightElf: int = auto()
    Undead: int = auto()
    Tauren: int = auto()
    Gnome: int = auto()
    Troll: int = auto()
    Goblin: int = auto()
    BloodElf: int = auto()
    Draenei: int = auto()


class RequiredHonorRank(IntEnum):
    Undefined = 0
    Private_Scout = 1
    Corporal_Grunt = 2
    Sergeant_Sergeant = 3
    MasterSergeant_SeniorSergeant = 4
    SergeantMajor_FirstSergeant = 5
    Knight_StoneGuard = 6
    KnightLieutenant_BloodGuard = 7
    KnightCaptain_Legionnare = 8
    KnightChampion_Centurion = 9
    LieutenantCommander_Champion = 10
    Commander_LieutenantGeneral = 11
    Marshal_General = 12
    FieldMarshal_Warlord = 13
    GrandMarshal_HighWarlord = 14


class ReputationRank(IntEnum):
    Hated = 0
    Hostile = 1
    Unfriendly = 2
    Neutral = 3
    Friendly = 4
    Honored = 5
    Revered = 6
    Exalted = 7


class Requires(BaseModel):
    classes: list[AllowableClass | int] = Field(
        default=[],
        description=dedent(
            """
            Classes permitted to use the item.
            """,
        ),
    )
    races: list[AllowableRace | int] = Field(
        default=[],
        description=dedent(
            """
            Races permitted to use the item.
            """,
        ),
    )
    level: int = Field(
        default=1,
        description=dedent(
            """
            The minimum player level required to equip the item.
            """,
        ),
    )
    skill: LookupID = Field(
        default=0,
        description=dedent(
            """
            The skill required to use this item.
            """,
        ),
    )
    skillRank: int = Field(
        default=0,
        description=dedent(
            """
            The required skill rank the player needs to have to use this item.
            """,
        ),
    )
    spell: LookupID = Field(
        default=0,
        description=dedent(
            """
            The required spell that the player needs to have to use this item.
            """,
        ),
    )
    honorRank: (RequiredHonorRank | int) = Field(
        default=RequiredHonorRank.Undefined,
        description=dedent(
            """
            The required PvP rank required to use the item.",
            serialization_alias="requiredhonorrank",
            """,
        ),
    )
    cityRank: int = Field(
        default=0,
        description=dedent(
            """
            Unused. All items have this set to 0.
            """,
        ),
    )
    reputationFaction: int = Field(
        default=0,
        description=dedent(
            """
            The faction template ID of the faction that the player has to have
            a certain ranking with. If this value is 0, the faction of the
            seller of the item is used.
            """,
        ),
    )
    reputationRank: (ReputationRank | int) = Field(
        default=0,
        description=dedent(
            """
            The required reputation rank to use the item.
            """,
        ),
    )
    disenchantSkill: int = Field(
        default=0,
        description=dedent(
            """
            The required skill proficiency in disenchanting that the player must
            have in order to disenchant this item.
            """,
        ),
    )
    map: LookupID = Field(
        default=0,
        description=dedent(
            """
            The ID of the map in which this item can be used. If you leave the
            map, the item will be deleted from the inventory.
            """,
        ),
    )
    area: LookupID = Field(
        default=0,
        description=dedent(
            """
            The ID of the zone in which this item can be used. If you leave the
            area, the item will be deleted from the inventory.
            """,
        ),
    )
    holiday: LookupID = Field(
        default=0,
        description=dedent(
            """
            The holiday event that must be active in order to use the item.
            """,
        ),
    )

    @staticmethod
    def from_sql(
        classes: str = "AllowableClass",
        races: str = "AllowableRace",
        level: str = "RequiredLevel",
        skill: str = "RequiredSkill",
        skillRank: str = "RequiredSkillRank",
        spell: str = "requiredspell",
        honorRank: str = "requiredhonorrank",
        cityRank: str = "RequiredCityRank",
        reputationFaction: str = "RequiredReputationFaction",
        reputationRank: str = "RequiredReputationRank",
        disenchantSkill: str = "RequiredDisenchantSkill",
        map: str = "Map",
        area: str = "area",
        holiday: str = "HolidayId",
    ):
        def from_sql(
            sql_dict: dict[str, any],
            cursor: Cursor,
            field_type: type,
        ) -> "Requires":
            return Requires(
                classes=IntFlagUtils.resolve(sql_dict[races], AllowableRace),
                races=IntFlagUtils.resolve(sql_dict[classes], AllowableClass),
                level=sql_dict[level],
                skill=sql_dict[skill],
                skillRank=sql_dict[skillRank],
                spell=sql_dict[spell],
                honorRank=sql_dict[honorRank],
                cityRank=sql_dict[cityRank],
                reputationFaction=sql_dict[reputationFaction],
                reputationRank=sql_dict[reputationRank],
                disenchantSkill=sql_dict[disenchantSkill],
                map=sql_dict[map],
                area=sql_dict[area],
                holiday=sql_dict[holiday],
            )
        return from_sql

    @staticmethod
    def to_sql(
        classes: str = "AllowableClass",
        races: str = "AllowableRace",
        level: str = "RequiredLevel",
        skill: str = "RequiredSkill",
        skillRank: str = "RequiredSkillRank",
        spell: str = "requiredspell",
        honorRank: str = "requiredhonorrank",
        cityRank: str = "RequiredCityRank",
        reputationFaction: str = "RequiredReputationFaction",
        reputationRank: str = "RequiredReputationRank",
        disenchantSkill: str = "RequiredDisenchantSkill",
        map: str = "Map",
        area: str = "area",
        holiday: str = "HolidayId",
    ):
        def to_sql(
            model_field: str,
            model_dict: dict[str, any],
            cursor: Cursor,
            field_type: type,
        ) -> dict[str, any]:
            r: "Requires" = model_dict[model_field]
            return {
                classes: sum(r.classes),
                races: sum(r.races),
                level: r.level,
                skill: int(r.skill),
                skillRank: int(r.skillRank),
                spell: int(r.spell),
                honorRank: int(r.honorRank),
                cityRank: int(r.cityRank),
                reputationFaction: int(r.reputationFaction),
                reputationRank: int(r.reputationRank),
                disenchantSkill: int(r.disenchantSkill),
                map: int(r.map),
                area: int(r.area),
                holiday: int(r.holiday),
            }
        return to_sql
