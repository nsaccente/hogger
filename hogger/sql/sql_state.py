from hogger import Entity

class SQLState:
    id: str
    data: dict

    @staticmethod
    def from_entity(e: Entity):
        print(e.model_dump())