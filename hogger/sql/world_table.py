import mysql.connector
from hogger import Item, Entity
import logging
from inspect import cleandoc


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
                    db_key INT NOT NULL,
                    hogger_identifier VARCHAR(128) NOT NULL,
                    PRIMARY KEY (entity_type, db_key, hogger_identifier)
                );
                """
            )


    def get_entities(self):
        """
        Gets all entities managed by Hogger from the world database.
        """
        with self._cnx.cursor(buffered=True) as cursor:
            cursor.execute(
                """
                SELECT entity_type, db_key, hogger_identifier
                FROM hoggerstate;
                """
            )
            states = cursor.fetchall()
            hoggerstates = []
            for entity_type, db_key, hogger_identifier in states:

                # Map a entity_type id from hoggerstate to an Entity object
                match entity_type:
                    case 0:
                        hoggerstates.append(
                            ENTITY_TYPE_MAP
                            [entity_type]
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
            return hoggerstates


    def write_test(self, _type: int, id: int, name: str):
        with self._cnx.cursor(buffered=True) as cursor:
            cursor.execute(
                f"""
                REPLACE INTO hoggerstate (entity_type, db_key, hogger_identifier)
                VALUES ({_type}, {id}, "{name}");
                """
            )
            self._cnx.commit()