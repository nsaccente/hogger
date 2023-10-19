import logging
from inspect import cleandoc

import mysql.connector

from hogger.entities import Entity
from hogger.entities.entity_codes import EntityCodes
from hogger.engine import State


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
        self.database=database
        if not self._cnx.is_connected():
            raise Exception(f"Unable to connect to worldserver database '{database}'")

        # Initialize the hoggerstate table if one doesn't already exist.
        with self._cnx.cursor() as cursor:
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS hoggerstate (
                    entity_code INT NOT NULL,
                    hogger_identifier VARCHAR(128) NOT NULL,
                    db_key INT NOT NULL,
                    PRIMARY KEY (entity_code, hogger_identifier)
                );
                """
            )

            cursor.execute(
                f"""
                SELECT * 
                FROM information_schema.tables
                WHERE table_schema = '{self.database}'
                    AND table_name = 'hoggerlock'
                LIMIT 1;
                """
            )
            exists = len(cursor.fetchall()) > 0
            if not exists:
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS hoggerlock (
                        k VARCHAR(32) NOT NULL,
                        v BIT NOT NULL,
                        PRIMARY KEY (k)
                    );
                    """
                )
                cursor.execute(
                    """
                    INSERT INTO hoggerlock(k, v) values ("locked", 0);
                    """
                )


    def get_hoggerstate(self) -> State:   
        with self._cnx.cursor(buffered=True) as cursor:
            cursor.execute(
                """
                SELECT entity_code, hogger_identifier, db_key
                FROM hoggerstate;
                """
            )
        hoggerstates = cursor.fetchall()
        actual = State()
        for entity_code, hogger_identifier, db_key in hoggerstates:
            actual[entity_code][hogger_identifier] = (
                self.resolve_hoggerstate(
                    entity_code=entity_code, 
                    hogger_identifier=hogger_identifier,
                    db_key=db_key, 
                )
            )
        return actual


    def resolve_hoggerstate(
        self,
        entity_code: int,
        hogger_identifier: str,
        db_key: int,
    ) -> Entity:
        """
        Gets all entities managed by Hogger from the world database.
        """
        if entity_code in EntityCodes:
            return (
                EntityCodes[entity_code]
                .from_hoggerstate(
                    db_key=db_key,
                    hogger_identifier=hogger_identifier,
                    cursor=self._cnx.cursor(),
                )
            )
        else:
            logging.warning(
                cleandoc(
                    f"""
                    During parsing of hoggerstate table, encountered the
                    entity_entity_code '{entity_code}', which isn't mappable to an
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
        entity_code: int, 
        hogger_identifier: str, 
        db_key: int,
    ):
        with self._cnx.cursor(buffered=True) as cursor:
            cursor.execute(
                f"""
                REPLACE INTO hoggerstate (entity_code, hogger_identifier, db_key)
                VALUES ({entity_code}, "{hogger_identifier}", {db_key});
                """
            )
            self._cnx.commit()


    def is_locked(self) -> bool:
        with self._cnx.cursor() as cursor:
            cursor.execute(
                """
                SELECT * FROM hoggerlock
                WHERE k="locked";
                """
            )
            # TODO: Raise error if this returns nil
            return bool(cursor.fetchone()[1])


    def acquire_lock(self):
        with self._cnx.cursor() as cursor:
            cursor.execute(
                """
                REPLACE INTO hoggerlock(k, v)
                VALUES ("locked", 1);
                """
            )
            self._cnx.commit()


    def release_lock(self):
        with self._cnx.cursor() as cursor:
            cursor.execute(
                """
                REPLACE INTO hoggerlock(k, v)
                VALUES ("locked", 0);
                """
            )
            self._cnx.commit()
