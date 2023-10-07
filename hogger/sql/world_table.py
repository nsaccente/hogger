import mysql.connector
from hogger import Item, Entity
from enum import Enum


class WorldTable:
    # Dict used to map entity types to their code in the hoggerstate table. We
    # don't bother mapping entity aliases here since they'll map back to the
    # same table in the world database.
    ENTITY_TABLE_MAP: dict[int, Entity] = {
        0: Item
    }

    def __init__(
        self,
        host: str,
        port: (str | int),
        database: str,
        user: str,
        password: str,
    ) -> None:
        self._cnx = mysql.connector.connect(
            host=host,
            port=port,
            database=database,
            user=user,
            password=password,
        )
        if not self._cnx.is_connected():
            raise Exception(f"Unable to connect to worldserver database '{database}'")

        with self._cnx.cursor() as cursor:
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS hoggerstate (
                    table_key INT NOT NULL,
                    db_key INT NOT NULL,
                    hogger_identifier VARCHAR(128) NOT NULL,
                    PRIMARY KEY (type, id)
                );
                """
            )
        

    def get_hoggerstate(self):
        with self._cnx.cursor(buffered=True) as cursor:
            cursor.execute("SELECT type, id, name FROM hoggerstate;")
            states = cursor.fetchall()
            for state in states:
                EntityType = WorldTable.ENTITY_TABLE_MAP[state[0]]
                id = state[1]
                cursor.execute(
                    f"""
                    SELECT * FROM {EntityType.table_name()}
                    WHERE `{EntityType.db_key()}`={id};
                    """
                )
                entity = cursor.fetchall()
                # There must be exactly one event returned, since there the id should be the unique key.
                assert(len(entity) == 1)
                print(entity)


    def write_test(self, _type: int, id: int, name: str):
        with self._cnx.cursor(buffered=True) as cursor:
            cursor.execute(
                f"""
                REPLACE INTO hoggerstate (type, id, name)
                VALUES ({_type}, {id}, "{name}");
                """
            )
            self._cnx.commit()