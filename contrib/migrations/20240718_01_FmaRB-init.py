"""
Init
"""

from yoyo import step

__depends__ = {}

steps = [
    step(
    """
        create table admin(
            id bigint primary key generated always as identity,
            name varchar(512) not null unique,
            date_create timestamp without time zone not null default now(),
            date_update timestamp without time zone not null default now()
        )
    """, "drop table admin"
    ),
]
