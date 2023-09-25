from pydantic import BaseModel, Field

class PageText(BaseModel):
    id: int = Field(
        default=0,
        serialization_alias="ID",
        ge=0,
    )
    text: str = Field(
        default="",
        serialization_alias="Text",
    )
    nextPageId: int = Field(
        default=0,
        serialization_alias="Next Page I D",
        ge=0,
    )
    verifiedBuild: str = Field(
        default=1,
        serialization_alias="Verified Build",
    )


class ItemLimitCategory(BaseModel):
    id: int = Field(
        default=0,
        validation_alias="ID",
    )
    name: str = Field(
        validation_alias="Name",
    )
    count: int = Field(
        default=1,
        validation_alias="Count",
    )
    isGem: bool = Field(default=False, validation_alias="IsGem")


class ItemLimitCategory(BaseModel):
    id: int = Field(
        default=0,
        serialization_alias="ID",
    )
    name: str = Field(
        serialization_alias="Name",
    )
    count: int = Field(
        default=1,
        serialization_alias="Count",
    )
    isGem: bool = Field(
        default=False,
        serialization_alias="IsGem",
    )
