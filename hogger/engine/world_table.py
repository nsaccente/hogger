import copy
import logging
from inspect import cleandoc

import mysql.connector

from hogger.entities import Entity
from hogger.entities.entity_codes import EntityCodes

from .sql import Queries


class State(dict[int, dict[str, (Entity | dict[str, any])]]):
    def __init__(self):
        super().__init__({entity_code: {} for entity_code, _ in EntityCodes.items()})


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
        self._created = None
        self._modified = None
        self._changes = None
        self._unchanged = None
        self._deleted = None

        self.database = database
        if not self._cnx.is_connected():
            # TODO: Add better description
            raise Exception(f"Unable to connect to worldserver database '{database}'")

        # Initialize the hoggerstate table if one doesn't already exist.
        with self._cnx.cursor() as cursor:
            for init_query in Queries.init():
                cursor.execute(init_query)
        self._actual_state: State = self._get_actual_state()
        self._desired_state: State = State()

    def is_locked(self) -> bool:
        with self._cnx.cursor() as cursor:
            cursor.execute(
                """
                SELECT * FROM hoggerlock
                WHERE k="locked";
                """,
            )
            # TODO: Raise error if this returns nil
            return bool(cursor.fetchone()[1])

    def acquire_lock(self):
        with self._cnx.cursor() as cursor:
            cursor.execute(
                """
                REPLACE INTO hoggerlock(k, v)
                VALUES ("locked", 1);
                """,
            )
            self._cnx.commit()

    def release_lock(self) -> None:
        with self._cnx.cursor() as cursor:
            cursor.execute(
                """
                REPLACE INTO hoggerlock(k, v)
                VALUES ("locked", 0);
                """,
            )
            self._cnx.commit()

    def _get_actual_state(self) -> State:
        with self._cnx.cursor(buffered=True) as cursor:
            cursor.execute(
                """
                SELECT entity_code, hogger_identifier, db_key
                FROM hoggerstate;
                """,
            )
        hoggerstates = cursor.fetchall()
        actual = State()
        for entity_code, hogger_identifier, db_key in hoggerstates:
            actual[entity_code][hogger_identifier] = self.resolve_hoggerstate(
                entity_code=entity_code,
                hogger_identifier=hogger_identifier,
                db_key=db_key,
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
            return EntityCodes[entity_code].from_hoggerstate(
                db_key=db_key,
                hogger_identifier=hogger_identifier,
                cursor=self._cnx.cursor(),
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
                    """,
                ),
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
                """,
            )
            self._cnx.commit()

    def add_desired(self, *entities: Entity) -> None:
        for entity in entities:
            entity_code = EntityCodes(type(entity))
            hogger_identifier = entity.hogger_identifier()
            self._desired_state[entity_code][hogger_identifier] = entity

    def _stage_str(self) -> str:
        s: list[str] = []

        s.append("To be Created:")
        for entity_code in self._created:
            entity_type = EntityCodes[entity_code].__name__
            for hogger_id in self._created[entity_code]:
                s.append(f"  {entity_type}.{hogger_id}")

        s.append("\nTo Be Modified:")
        for entity_code in self._modified:
            entity_type = EntityCodes[entity_code].__name__
            for hogger_id in self._modified[entity_code]:
                s.append(f"  {entity_type}.{hogger_id}")
                for f, delta in self._changes[entity_code][hogger_id].items():
                    s.append(f"    {f}")
                    # TODO: Format changes in a clearer fashion.
                    s.append(f"      desired: {str(delta['desired'])}")
                    s.append(f"      actual:  {str(delta['actual'])}")

        s.append("\nUnchanged:")
        for entity_code in self._unchanged:
            entity_type = EntityCodes[entity_code].__name__
            for hogger_id in self._unchanged[entity_code]:
                s.append(f"  {entity_type}.{hogger_id}")

        s.append("\nTo Be Deleted:")
        for entity_code in self._deleted:
            entity_type = EntityCodes[entity_code].__name__
            for hogger_id in self._deleted[entity_code]:
                s.append(f"  {entity_type}.{hogger_id}")

        return "\n".join(s)

    def stage(self) -> str:
        self._created = State()
        self._modified = State()
        self._changes = State()
        self._unchanged = State()
        self._deleted = copy.deepcopy(self._actual_state)
        for entity_code in EntityCodes:
            for hogger_id, des_entity in self._desired_state[entity_code].items():
                # If hogger_id from desired state exists in actual state,
                # compute the diff; otherwise, add to `created`.
                if hogger_id in self._actual_state[entity_code]:
                    # If the diff returned has contents in it, add to
                    # `modified`. Otherwise, no action necessary.
                    modified_entity, mod_changes = des_entity.diff(
                        self._actual_state[entity_code][hogger_id],
                    )
                    if len(mod_changes) > 0:
                        # If any changes are returned from the calling
                        # Entity.diff, add add the item to the `modified` dict,
                        # and store the changes in the dict that will be
                        # returned.
                        self._modified[entity_code][hogger_id] = modified_entity
                        self._changes[entity_code][hogger_id] = mod_changes
                    else:
                        # We don't need to store the unchanged entity, since we
                        # aren't going to do anything with it.
                        self._unchanged[entity_code][hogger_id] = None
                    del self._deleted[entity_code][hogger_id]
                else:
                    des_entity.set_db_key(60000)
                    self._created[entity_code][hogger_id] = des_entity
        return self._stage_str()

    def apply(
        self,
    ) -> None:
        with self._cnx.cursor() as cursor:
            for entity_code in EntityCodes:
                for _, entity in self._created[entity_code].items():
                    entity.apply(cursor)

                for _, entity in self._modified[entity_code].items():
                    entity.apply(cursor)

                for _, entity in self._deleted[entity_code].items():
                    entity.apply(cursor)
        self._cnx.commit()
