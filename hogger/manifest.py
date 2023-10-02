import json
from typing import Union

import yaml
from pydantic import BaseModel, Field
from typing_extensions import Annotated

from hogger.entities.items import OneHandedAxe, TwoHandedAxe

Entity = Annotated[Union[OneHandedAxe, TwoHandedAxe], Field(discriminator="type")]


class Manifest(BaseModel):
    apiVersion: str = Field(
        description="API version to use against the configuration file.",
    )
    entities: list[Entity]

    @staticmethod
    def from_file(filepath: str) -> "Manifest":
        with open(filepath, "r") as yaml_file:
            return Manifest(**yaml.safe_load(yaml_file))

    def yaml_dump(
        self,
        by_alias: bool = False,
        exclude_unset: bool = True,
    ) -> str:
        return yaml.dump(
            json.loads(
                self.model_dump_json(
                    by_alias=by_alias,
                    exclude_unset=True,
                )
            ),
            indent=2,
            sort_keys=False,
        )
