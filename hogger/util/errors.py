from typing import Any


class InvalidValueException(Exception):
    def __init__(
        self,
        field_name: str,
        FieldType: type,
        expected_values: list[str],
        actual: Any,
        suggestion: Any = None,
    ) -> None:
        e = (
            f"Invalid value for {FieldType.__name__} field '{field_name}'; valid values are "
            f"{expected_values}, or an integer, got '{actual}'"
        )
        if suggestion is not None:
            e += f".\n\nDid you mean '{suggestion}' for field '{field_name}'?"
        super().__init__(e)
