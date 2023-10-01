from typing import Any

from pydantic import BaseModel, Field, model_validator

from src.misc.misc import LookupID


class ItemSockets(BaseModel):
    bonus: LookupID = Field(default=0, ge=0)
    properties: LookupID = Field(default=0, ge=0)
    meta: int = Field(
        default=0,
        description="The number of meta sockets. Default is 0.",
        ge=0,
    )
    blue: int = Field(
        default=0,
        description="The number of blue sockets. Default is 0.",
        ge=0,
    )
    yellow: int = Field(
        default=0,
        description="The number of yellow sockets. Default is 0.",
        ge=0,
    )
    red: int = Field(
        default=0,
        description="The number of red sockets. Default is 0.",
        ge=0,
    )

    # TODO
    @model_validator(mode="before")
    def ensure_3_of_4_socket_colors(cls, data: Any) -> Any:
        return data
