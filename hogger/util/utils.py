from typing import Union



def _get_all_subclasses(cls) -> list[type]:
    subclasses = []
    for subclass in cls.__subclasses__():
        subclasses.append(subclass)
        subclasses.extend(_get_all_subclasses(subclass))
    return subclasses


def pydantic_annotation(cls) -> type:
    subclasses = _get_all_subclasses(cls)
    FinalType = Union[subclasses[0], subclasses[1]]
    for subclass in subclasses[2:]:
        FinalType = Union[FinalType, subclass]
    return FinalType

