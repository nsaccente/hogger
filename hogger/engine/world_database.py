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


class WorldDatabase:
    def __init__(
        self,
        host: str,
        port: (str | int),
        database: str,
        user: str,
        password: str,
    ) -> None:
        # Create a connection tied to the WorldDatabase object.
        self._cnx = mysql.connector.connect(
            host=host,
            port=port,
            database=database,
            user=user,
            password=password,
        )
        self.database = database
        if not self._cnx.is_connected():
            raise Exception(f"Unable to connect to world database '{database}'")

        # Initialize the hoggerstate table if one doesn't already exist.
        with self._cnx.cursor() as cursor:
            for init_query in Queries.init():
                cursor.execute(init_query)
        self._actual_state: State = self._get_actual_state()
        self._desired_state: State = State()
        self._id_iters: dict[str, dict[str, iter]] = dict()
        self.staged_inserts: list[str] = []
        self.staged_deletes: list[str] = []

    def next_id(self, table: str, field: str) -> iter:
        def _next_id_iter(ids: list):
            id = 0
            while True:
                # TODO: This can probably be more efficient.
                if id not in ids:
                    yield id
                id += 1

        if table not in self._id_iters:
            self._id_iters[table] = {}
        ids = []
        if field not in self._id_iters[table]:
            with self._cnx.cursor(buffered=True) as cursor:
                cursor.execute(f"SELECT {field} FROM {table} ORDER BY {field};")
                fetchall = cursor.fetchall()
                # If there are no entries in `table`, fetchall returns an empty
                # list. If there are entries, we parse them out to list[int]
                if len(fetchall) > 0:
                    ids.extend(list(zip(*fetchall))[0])
                self._id_iters[table][field] = _next_id_iter(ids)
        return next(self._id_iters[table][field])

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

    def _stage_str(
        self,
        created: State(),
        modified: State(),
        changes: State(),
        unchanged: State(),
        deleted: State(),
    ) -> str:
        s: list[str] = []

        s.append("To be Created:")
        for entity_code in created:
            entity_type = EntityCodes[entity_code].__name__
            for hogger_id in created[entity_code]:
                s.append(f"  {entity_type}.{hogger_id}")

        s.append("\nTo Be Modified:")
        for entity_code in modified:
            entity_type = EntityCodes[entity_code].__name__
            for hogger_id in modified[entity_code]:
                s.append(f"  {entity_type}.{hogger_id}")
                for f, delta in changes[entity_code][hogger_id].items():
                    s.append(f"    {f}")
                    # TODO: Format changes in a clearer fashion.
                    s.append(f"      desired: {str(delta['desired'])}")
                    s.append(f"      actual:  {str(delta['actual'])}")

        s.append("\nUnchanged:")
        for entity_code in unchanged:
            entity_type = EntityCodes[entity_code].__name__
            for hogger_id in unchanged[entity_code]:
                s.append(f"  {entity_type}.{hogger_id}")

        s.append("\nTo Be Deleted:")
        for entity_code in deleted:
            entity_type = EntityCodes[entity_code].__name__
            for hogger_id in deleted[entity_code]:
                s.append(f"  {entity_type}.{hogger_id}")

        return "\n".join(s)

    def stage(self) -> str:
        created = State()
        modified = State()
        changes = State()
        unchanged = State()
        deleted = copy.deepcopy(self._actual_state)
        des_entity: Entity

        with self._cnx.cursor() as cursor:
            self._cnx.commit()
            for entity_code in EntityCodes:
                for hogger_id, des_entity in self._desired_state[entity_code].items():
                    # If hogger_id from desired state exists in actual state,
                    # compute the diff; otherwise, add to `created`.
                    if hogger_id in self._actual_state[entity_code]:
                        actual_entity: Entity = self._actual_state[entity_code][
                            hogger_id
                        ]
                        mod_changes: dict[str, any]
                        des_entity, mod_changes = des_entity.diff(actual_entity)
                        if len(mod_changes) > 0:
                            # MODIFY
                            changes[entity_code][hogger_id] = mod_changes
                            modified[entity_code][hogger_id] = des_entity
                            self.staged_deletes.extend(actual_entity.delete(cursor))
                            self.staged_inserts.extend(des_entity.insert(cursor))
                        else:
                            # UNCHANGED
                            unchanged[entity_code][hogger_id] = None
                        # Finally, remove from `deleted`
                        del deleted[entity_code][hogger_id]
                    else:
                        # CREATE
                        if des_entity.id < 0:
                            des_entity.update_id(cursor, next_id_iterfunc=self.next_id)
                        created[entity_code][hogger_id] = des_entity
                        self.staged_inserts.extend(des_entity.insert(cursor))

            # DELETE
            for entity_code in EntityCodes:
                for _, entity in deleted[entity_code].items():
                    self.staged_deletes.extend(entity.delete(cursor))

        return self._stage_str(
            created=created,
            modified=modified,
            changes=changes,
            unchanged=unchanged,
            deleted=deleted,
        )

    def commit(self) -> None:
        try:
            cursor = self._cnx.cursor()
            for query in self.staged_inserts:
                # print(query)
                cursor.execute(query)
            for query in self.staged_deletes:
                # print(query)
                cursor.execute(query)
            self._cnx.commit()
        except Exception as e:
            self._cnx.rollback()
            raise
        finally:
            cursor.close()
