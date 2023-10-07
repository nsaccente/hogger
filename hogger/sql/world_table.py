import mysql.connector
from hogger import Item, Entity
import logging
from inspect import cleandoc


class Hoggerstate:
    table_key: int
    db_key: int
    hogger_key: str
    entity_type: type[Entity]

    def __new__(cls, table_key: int, db_key: int, hogger_key: str) -> None:
        match table_key:
            case 0:   
                cls.entity_type = Item
            case _:
                logging.warning(
                    cleandoc(
                        f"""
                        During parsing of hoggerstate table, encountered the
                        table_key '{table_key}', which isn't mappable to an 
                        entity type.

                        It's possible that the hoggerstate table has entries
                        that were created using a different version of Hogger.
                        Make sure that you're using a version that is compatible
                        with the version used to manage the hoggerstate table.
                        Check your version of hogger using `hogger version`.
                        """

                    )
                )
                return None
        cls.table_key = table_key
        cls.db_key = db_key
        cls.hoger_key = hogger_key
        return cls


class WorldTable:
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
            entities: dict[Hoggerstate, Entity]= {}
            for state in states:
                hs = Hoggerstate(*state)
                if hs is not None: 
                    entities[hs] = hs.entity_type.from_hoggerstate(
                        
                    )


    def write_test(self, _type: int, id: int, name: str):
        with self._cnx.cursor(buffered=True) as cursor:
            cursor.execute(
                f"""
                REPLACE INTO hoggerstate (type, id, name)
                VALUES ({_type}, {id}, "{name}");
                """
            )
            self._cnx.commit()