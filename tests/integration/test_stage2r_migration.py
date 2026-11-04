"""Upgrade, rollback and database constraints on disposable PostgreSQL databases."""

import json
from concurrent.futures import ThreadPoolExecutor
from threading import Event
from uuid import uuid4

import pytest
from alembic import command
from alembic.config import Config
from conftest import migrate
from sqlalchemy import create_engine, text
from sqlalchemy.exc import DBAPIError


def seed_legacy(database, *, corrected=False):
    tutor, first, second, source, observation = (uuid4() for _ in range(5))
    engine = create_engine(database.database_url)
    try:
        with engine.begin() as connection:
            connection.execute(
                text("INSERT INTO learners(id,tutor_id,profile_revision) VALUES (:id,:tutor,1)"),
                [{"id": first, "tutor": tutor}, {"id": second, "tutor": tutor}],
            )
            connection.execute(
                text("""INSERT INTO sources(id,learner_id,tutor_id,kind,qualification,raw_text,
                    fingerprint) VALUES (:id,:learner,:tutor,'lesson','tutor_notes',
                                         'SYNTHETIC','x')"""),
                {"id": source, "learner": first, "tutor": tutor},
            )
            if corrected:
                connection.execute(
                    text("""INSERT INTO source_history
                      (source_id,learner_id,tutor_id,revision,kind,occurred_at,qualification,
                       raw_text,expires_at,fingerprint)
                      SELECT id,learner_id,tutor_id,revision,kind,occurred_at,qualification,
                             raw_text,expires_at,fingerprint FROM sources""")
                )
                connection.execute(text("UPDATE sources SET revision=2"))
            connection.execute(
                text("""INSERT INTO observations(id,revision,learner_id,tutor_id,source_id,
                    confirmed,data)
                    VALUES (:id,1,:learner,:tutor,:source,true,CAST(:data AS jsonb))"""),
                {
                    "id": observation,
                    "learner": first,
                    "tutor": tutor,
                    "source": source,
                    "data": json.dumps({"source_id": str(source)}),
                },
            )
    finally:
        engine.dispose()
    return tutor, first, second, source, observation


def downgrade(database):
    engine = create_engine(database.database_url)
    try:
        with engine.begin() as connection:
            config = Config("alembic.ini")
            config.attributes["connection"] = connection
            command.downgrade(config, "0005")
    finally:
        engine.dispose()


def test_migration_preserves_unambiguous_data_and_enforces_same_learner(database):
    migrate(database, "0005")
    tutor, first, second, source, observed = seed_legacy(database)
    migrate(database)
    admin = create_engine(database.database_url)
    try:
        with admin.connect() as connection:
            assert connection.execute(
                text("SELECT learner_id,source_id,revision,raw_text FROM source_versions")
            ).one() == (first, source, 1, "SYNTHETIC")
            assert connection.execute(
                text("SELECT learner_id,id,source_revision FROM observations")
            ).one() == (first, observed, 1)
        with pytest.raises(DBAPIError):
            with admin.begin() as connection:
                connection.execute(text("SET LOCAL ROLE tutor_app"))
                connection.execute(
                    text("SELECT set_config('app.tutor_id',:tutor,true)"), {"tutor": str(tutor)}
                )
                connection.execute(
                    text("""INSERT INTO observations
                        (id,revision,learner_id,tutor_id,source_id,source_revision,confirmed,data)
                        VALUES (:id,1,:learner,:tutor,:source,1,true,CAST(:data AS jsonb))"""),
                    {
                        "id": uuid4(),
                        "learner": second,
                        "tutor": tutor,
                        "source": source,
                        "data": json.dumps({"source_id": str(source)}),
                    },
                )
        downgrade(database)
        with admin.connect() as connection:
            assert connection.scalar(text("SELECT version_num FROM alembic_version")) == "0005"
            assert connection.scalar(text("SELECT raw_text FROM sources")) == "SYNTHETIC"
            assert connection.scalar(text("SELECT count(*) FROM observations")) == 1
    finally:
        admin.dispose()


def test_migration_stops_without_guessing_ambiguous_provenance(database):
    migrate(database, "0005")
    seed_legacy(database, corrected=True)
    with pytest.raises(DBAPIError, match="ambiguous evidence source revision"):
        migrate(database)
    admin = create_engine(database.database_url)
    try:
        with admin.connect() as connection:
            assert connection.scalar(text("SELECT version_num FROM alembic_version")) == "0005"
            assert connection.scalar(text("SELECT revision FROM sources")) == 2
            assert connection.scalar(text("SELECT count(*) FROM source_history")) == 1
            assert connection.scalar(text("SELECT count(*) FROM observations")) == 1
    finally:
        admin.dispose()


def test_migration_rejects_cross_learner_legacy_reference(database):
    migrate(database, "0005")
    _, _, second, _, _ = seed_legacy(database)
    admin = create_engine(database.database_url)
    try:
        with admin.begin() as connection:
            connection.execute(
                text("UPDATE observations SET learner_id=:learner"), {"learner": second}
            )
        with pytest.raises(DBAPIError, match="mismatched learner or tutor source references"):
            migrate(database)
        with admin.connect() as connection:
            assert connection.scalar(text("SELECT version_num FROM alembic_version")) == "0005"
            assert connection.scalar(text("SELECT learner_id FROM observations")) == second
    finally:
        admin.dispose()


def test_migration_rejects_head_without_its_history(database):
    migrate(database, "0005")
    seed_legacy(database, corrected=True)
    admin = create_engine(database.database_url)
    try:
        with admin.begin() as connection:
            connection.execute(text("DELETE FROM source_history"))
        with pytest.raises(DBAPIError, match="ambiguous evidence source revision"):
            migrate(database)
        with admin.connect() as connection:
            assert connection.scalar(text("SELECT version_num FROM alembic_version")) == "0005"
            assert connection.scalar(text("SELECT revision FROM sources")) == 2
            assert connection.scalar(text("SELECT count(*) FROM observations")) == 1
    finally:
        admin.dispose()


def test_restricted_writer_cannot_mutate_versions_or_hide_json_references(database):
    migrate(database, "0005")
    tutor, first, second, source, observed = seed_legacy(database)
    migrate(database)
    admin = create_engine(database.database_url)
    try:
        second_source = uuid4()
        with admin.begin() as connection:
            connection.execute(
                text(
                    "INSERT INTO sources(id,learner_id,tutor_id,revision) "
                    "VALUES (:id,:learner,:tutor,1)"
                ),
                {"id": second_source, "learner": second, "tutor": tutor},
            )
            connection.execute(
                text("""INSERT INTO source_versions
                  (learner_id,source_id,revision,tutor_id,kind,qualification,expires_at,fingerprint)
                  VALUES (:learner,:id,1,:tutor,'lesson','tutor_notes',
                          now()+interval '30 days','x')"""),
                {"id": second_source, "learner": second, "tutor": tutor},
            )
        for statement in (
            "UPDATE source_versions SET kind='homework'",
            "DELETE FROM source_versions",
            "DELETE FROM sources",
        ):
            with pytest.raises(DBAPIError, match="permission denied"):
                with admin.begin() as connection:
                    connection.execute(text("SET LOCAL ROLE tutor_app"))
                    connection.execute(
                        text("SELECT set_config('app.tutor_id',:tutor,true)"), {"tutor": str(tutor)}
                    )
                    connection.execute(text(statement))

        # JSON cannot claim a foreign linked observation while scalar columns are empty,
        # and it cannot disagree with the constrained source column.
        for payload in (
            {
                "source_id": str(second_source),
                "observation_id": str(observed),
                "observation_revision": 1,
            },
            {"source_id": str(uuid4()), "observation_id": None, "observation_revision": None},
        ):
            with pytest.raises(DBAPIError, match="check constraint"):
                with admin.begin() as connection:
                    connection.execute(text("SET LOCAL ROLE tutor_app"))
                    connection.execute(
                        text("SELECT set_config('app.tutor_id',:tutor,true)"), {"tutor": str(tutor)}
                    )
                    connection.execute(
                        text("""INSERT INTO activities
                          (id,revision,learner_id,tutor_id,source_id,source_revision,confirmed,data)
                          VALUES (:id,1,:learner,:tutor,:source,1,true,CAST(:data AS jsonb))"""),
                        {
                            "id": uuid4(),
                            "learner": second,
                            "tutor": tutor,
                            "source": second_source,
                            "data": json.dumps(payload),
                        },
                    )
        with admin.connect() as connection:
            assert (
                connection.scalar(text("SELECT count(*) FROM source_versions WHERE kind<>'lesson'"))
                == 0
            )
            assert connection.scalar(text("SELECT count(*) FROM activities")) == 0
            assert (
                connection.scalar(
                    text("SELECT count(*) FROM learners WHERE id=:id"), {"id": second}
                )
                == 1
            )
    finally:
        admin.dispose()


def test_upgrade_locks_out_legacy_writes_before_auditing(database):
    migrate(database, "0005")
    _, _, _, source, _ = seed_legacy(database)
    admin = create_engine(database.database_url)
    started = Event()

    def upgrade():
        started.set()
        migrate(database)

    try:
        with admin.begin() as writer:
            writer.execute(text("LOCK TABLE sources IN ROW EXCLUSIVE MODE"))
            with ThreadPoolExecutor(max_workers=1) as pool:
                future = pool.submit(upgrade)
                assert started.wait(2)
                for _ in range(200):
                    with admin.connect() as observer:
                        waiting = observer.scalar(
                            text("""SELECT count(*) FROM pg_stat_activity
                              WHERE datname=current_database() AND wait_event_type='Lock'
                              AND query LIKE '%LOCK TABLE learners, sources%'""")
                        )
                    if waiting:
                        break
                    Event().wait(0.01)
                assert waiting, "Migration did not wait for the legacy writer"
                writer.execute(text("UPDATE sources SET revision=2 WHERE id=:id"), {"id": source})
                writer.commit()
                with pytest.raises(DBAPIError, match="ambiguous evidence source revision"):
                    future.result(timeout=5)
        with admin.connect() as connection:
            assert connection.scalar(text("SELECT version_num FROM alembic_version")) == "0005"
            assert connection.scalar(text("SELECT revision FROM sources")) == 2
    finally:
        admin.dispose()


def test_downgrade_refuses_colliding_scoped_ids_without_losing_data(database):
    migrate(database, "0005")
    tutor, _, second, source, _ = seed_legacy(database)
    migrate(database)
    admin = create_engine(database.database_url)
    try:
        with admin.begin() as connection:
            connection.execute(
                text(
                    "INSERT INTO sources(id,learner_id,tutor_id,revision) "
                    "VALUES (:id,:learner,:tutor,1)"
                ),
                {"id": source, "learner": second, "tutor": tutor},
            )
            connection.execute(
                text("""INSERT INTO source_versions
                  (learner_id,source_id,revision,tutor_id,kind,qualification,expires_at,fingerprint)
                  VALUES (:learner,:id,1,:tutor,'lesson','tutor_notes',
                          now()+interval '30 days','x')"""),
                {"id": source, "learner": second, "tutor": tutor},
            )
        with pytest.raises(DBAPIError, match="learner-scoped identities collide"):
            downgrade(database)
        with admin.connect() as connection:
            assert connection.scalar(text("SELECT version_num FROM alembic_version")) == "0006"
            assert connection.scalar(text("SELECT count(*) FROM sources")) == 2
            assert connection.scalar(text("SELECT count(*) FROM source_versions")) == 2
            assert connection.scalar(text("SELECT count(*) FROM observations")) == 1
    finally:
        admin.dispose()


def test_downgrade_refuses_to_discard_evidence_version(database):
    migrate(database, "0005")
    tutor, first, _, source, _ = seed_legacy(database)
    migrate(database)
    admin = create_engine(database.database_url)
    try:
        with admin.begin() as connection:
            connection.execute(
                text("""INSERT INTO source_versions
                  (learner_id,source_id,revision,tutor_id,kind,qualification,expires_at,fingerprint)
                  VALUES (:learner,:id,2,:tutor,'lesson','transcript',
                          now()+interval '30 days','y')"""),
                {"id": source, "learner": first, "tutor": tutor},
            )
            connection.execute(text("UPDATE sources SET revision=2 WHERE id=:id"), {"id": source})
        with pytest.raises(DBAPIError, match="exact evidence provenance would be lost"):
            downgrade(database)
        with admin.connect() as connection:
            assert connection.scalar(text("SELECT version_num FROM alembic_version")) == "0006"
            assert connection.scalar(text("SELECT source_revision FROM observations")) == 1
            assert connection.scalar(text("SELECT count(*) FROM source_versions")) == 2
    finally:
        admin.dispose()


def test_source_version_rls_and_owner_deletion_cascade(database):
    migrate(database, "0005")
    tutor, first, _, _, _ = seed_legacy(database)
    migrate(database)
    admin = create_engine(database.database_url)
    try:
        with admin.begin() as connection:
            connection.execute(text("SET LOCAL ROLE tutor_app"))
            assert connection.scalar(text("SELECT count(*) FROM source_versions")) == 0
            connection.execute(
                text("SELECT set_config('app.tutor_id',:tutor,true)"), {"tutor": str(uuid4())}
            )
            assert connection.scalar(text("SELECT count(*) FROM source_versions")) == 0
            connection.execute(
                text("SELECT set_config('app.tutor_id',:tutor,true)"), {"tutor": str(tutor)}
            )
            assert connection.scalar(text("SELECT count(*) FROM source_versions")) == 1
            connection.execute(text("DELETE FROM learners WHERE id=:id"), {"id": first})
        with admin.connect() as connection:
            assert connection.scalar(text("SELECT count(*) FROM source_versions")) == 0
            assert connection.scalar(text("SELECT count(*) FROM observations")) == 0
            assert connection.scalar(text("SELECT count(*) FROM learners")) == 1
    finally:
        admin.dispose()


def test_downgrade_locks_out_source_correction_before_auditing(database):
    migrate(database, "0005")
    tutor, first, _, source, _ = seed_legacy(database)
    migrate(database)
    admin = create_engine(database.database_url)
    started = Event()

    def run_downgrade():
        started.set()
        downgrade(database)

    try:
        with admin.begin() as writer:
            writer.execute(text("LOCK TABLE sources IN ROW EXCLUSIVE MODE"))
            with ThreadPoolExecutor(max_workers=1) as pool:
                future = pool.submit(run_downgrade)
                assert started.wait(2)
                for _ in range(200):
                    with admin.connect() as observer:
                        waiting = observer.scalar(
                            text("""SELECT count(*) FROM pg_stat_activity
                              WHERE datname=current_database() AND wait_event_type='Lock'
                              AND query LIKE '%LOCK TABLE learners, sources, source_versions%'""")
                        )
                    if waiting:
                        break
                    Event().wait(0.01)
                assert waiting, "Downgrade did not wait for the source correction"
                writer.execute(
                    text("""INSERT INTO source_versions
                      (learner_id,source_id,revision,tutor_id,kind,qualification,expires_at,fingerprint)
                      VALUES (:learner,:id,2,:tutor,'lesson','transcript',
                              now()+interval '30 days','y')"""),
                    {"id": source, "learner": first, "tutor": tutor},
                )
                writer.execute(text("UPDATE sources SET revision=2 WHERE id=:id"), {"id": source})
                writer.commit()
                with pytest.raises(DBAPIError, match="exact evidence provenance would be lost"):
                    future.result(timeout=5)
        with admin.connect() as connection:
            assert connection.scalar(text("SELECT version_num FROM alembic_version")) == "0006"
            assert connection.scalar(text("SELECT source_revision FROM observations")) == 1
            assert connection.scalar(text("SELECT count(*) FROM source_versions")) == 2
    finally:
        admin.dispose()
