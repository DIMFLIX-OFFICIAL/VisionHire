import asyncpg
from alembic.config import Config
from alembic.runtime.environment import EnvironmentContext
from alembic.script import ScriptDirectory

import config as cfg




async def init_db():
    db = await asyncpg.connect(
        host=cfg.DB_HOST,
        port=cfg.DB_PORT,
        user=cfg.DB_USERNAME,
        password=cfg.DB_PASSWORD,
    )

    existing_databases = await db.fetch(
        "SELECT datname FROM pg_database WHERE datname = $1", cfg.DB_NAME
    )

    if not existing_databases:
        await db.execute(f'CREATE DATABASE "{cfg.DB_NAME}"')
        print(f"Database '{cfg.DB_NAME}' created successfully.")
    else:
        print(f"Database '{cfg.DB_NAME}' already exists.")

    await db.close()

    config = Config(cfg.PROJECT_ROOT / "alembic.ini")
    script = ScriptDirectory.from_config(config)
    head_revision = script.get_current_head()

    with EnvironmentContext(
        config,
        script,
        fn=lambda rev, _: script._upgrade_revs(head_revision, rev),
        as_sql=False,
        revision_environment=True,
        directives={},
    ):
        script.run_env()
        