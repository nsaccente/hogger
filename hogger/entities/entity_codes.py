from collections import OrderedDict

from .entity import Entity
from .item.item import Item


class EntityCodesDict(OrderedDict[int, Entity]):
    def __getattr__(self, item):
        return super().__getitem__(item)

    def __setattr__(self, item, value):
        return super().__setitem__(item, value)

    def __call__(self, entity: type) -> int:
        for type_code, type_anno in self.items():
            if issubclass(entity, type_anno):
                return type_code
        # TODO: Raise exception if the type isn't mappable.
        return -1


# When creating new entities, add them here with a unique code key.
EntityCodes = EntityCodesDict(
    {
        1: Item,
    },
)
