import logging
from inspect import cleandoc

import mysql.connector

from hogger.entities import Entity, Item

ENTITY_TYPE_MAP: dict[int, Entity] = {
    0: Item,
}

class WorldTable:
    def __init__(
        self,
        host: str,
        port: (str | int),
        database: str,
        user: str,
        password: str,
    ) -> None:
        # Create a connection tied to the WorldTable object.
        self._cnx = mysql.connector.connect(
            host=host,
            port=port,
            database=database,
            user=user,
            password=password,
        )
        if not self._cnx.is_connected():
            raise Exception(f"Unable to connect to worldserver database '{database}'")

        # Initialize the hoggerstate table if one doesn't already exist.
        with self._cnx.cursor() as cursor:
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS hoggerstate (
                    entity_type INT NOT NULL,
                    hogger_identifier VARCHAR(128) NOT NULL,
                    db_key INT NOT NULL,
                    PRIMARY KEY (entity_type, hogger_identifier)
                );
                """
            )


    def get_hoggerstate(self):   
        with self._cnx.cursor(buffered=True) as cursor:
            cursor.execute(
                """
                SELECT entity_type, hogger_identifier, db_key
                FROM hoggerstate;
                """
            )
        hoggerstate = cursor.fetchall()
        return hoggerstate


    def resolve_hoggerstate(
        self,
        entity_type: int,
        hogger_identifier: str,
        db_key: int,
    ) -> Entity:
        """
        Gets all entities managed by Hogger from the world database.
        """
        # Map a entity_type id from hoggerstate to an Entity object
        match entity_type:
            case 0:
                return (
                    ENTITY_TYPE_MAP[entity_type]
                    .from_hoggerstate(
                        db_key=db_key,
                        hogger_identifier=hogger_identifier,
                        cursor=self._cnx.cursor(),
                    )
                )
            case _:
                logging.warning(
                    cleandoc(
                        f"""
                        During parsing of hoggerstate table, encountered the
                        entity_type '{entity_type}', which isn't mappable to an
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


    def _write_hoggerstate(
        self, 
        entity_type: int, 
        hogger_identifier: str, 
        db_key: int,
    ):
        with self._cnx.cursor(buffered=True) as cursor:
            cursor.execute(
                f"""
                REPLACE INTO hoggerstate (entity_type, hogger_identifier, db_key)
                VALUES ({entity_type}, "{hogger_identifier}", {db_key});
                """
            )
            self._cnx.commit()
