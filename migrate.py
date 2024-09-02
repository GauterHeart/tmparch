import argparse
from argparse import ArgumentParser
from typing import Any

from yoyo import get_backend, read_migrations

from src.config import get_config


class NeedArgsException(Exception): ...


def parse_cli_args() -> argparse.Namespace:
    """Parse cli arguments."""

    parser = ArgumentParser(description="Apply migrations")
    parser.add_argument("--apply", action="store_true", help="Apply migrations")
    parser.add_argument("--fixtures", action="store_true", help="Fixtures")
    parser.add_argument("--rollback", action="store_true", help="Rollback migrations")
    parser.add_argument(
        "--rollback-one",
        action="store_true",
        help="Rollback one migration",
    )
    parser.add_argument(
        "--rollback-last",
        action="store_true",
        help="Rollback one migration",
    )
    parser.add_argument(
        "--reload",
        action="store_true",
        help="Rollback all migration and applying again",
    )
    args = parser.parse_args()
    return args


def _apply(backend: Any, migrations: Any) -> None:
    """Apply all migrations from `migrations`."""
    with backend.lock():
        # Apply any outstanding migrations
        backend.apply_migrations(backend.to_apply(migrations))


def _rollback(backend: Any, migrations: Any) -> None:
    """Rollback all migrations."""
    with backend.lock():
        # Rollback all migrations
        backend.rollback_migrations(backend.to_rollback(migrations))


def _rollback_one(backend: Any, migrations: Any) -> None:
    """Rollback one migration."""
    with backend.lock():
        effect = backend.to_rollback(migrations)
        if len(effect) == 0:
            print("No migrations")
            return

        for e in range(len(effect)):
            print(f"{e + 1}. {effect[e].id}")

        migration = input("Select migration: ")
        if not migration.isdecimal():
            print("Not valid num migration")
            return

        backend.rollback_one(effect[int(migration) - 1])


def _rollback_last(backend: Any, migrations: Any) -> None:
    """Rollback last migration."""
    with backend.lock():
        migrations = backend.to_rollback(migrations)
        for migration in migrations:
            backend.rollback_one(migration)
            break


def _reload(backend: Any, migrations: Any) -> None:
    """Rollback all and apply all migrations."""
    with backend.lock():
        backend.rollback_migrations(backend.to_rollback(migrations))
        backend.apply_migrations(backend.to_apply(migrations))


def main() -> None:
    config = get_config()
    args = parse_cli_args()
    # backend = get_backend(settings.POSTGRES.DSN)
    dsn = (
        f"postgresql://{config.POSTGRES_USER}:{config.POSTGRES_PASSWORD.get_secret_value()}"
        f"@{config.POSTGRES_HOST}:{config.POSTGRES_PORT}/{config.POSTGRES_DB}"
    )
    backend = get_backend(dsn)
    if args.fixtures is True:
        migration = read_migrations("contrib/fixtures")
    else:
        migration = read_migrations("contrib/migrations")
    if args.apply:
        _apply(backend=backend, migrations=migration)

    elif args.rollback:
        _rollback(backend=backend, migrations=migration)

    elif args.rollback_one:
        _rollback_one(backend=backend, migrations=migration)

    elif args.rollback_last:
        _rollback_last(backend=backend, migrations=migration)

    elif args.reload:
        _reload(backend=backend, migrations=migration)

    else:
        raise NeedArgsException()


if __name__ == "__main__":
    main()
