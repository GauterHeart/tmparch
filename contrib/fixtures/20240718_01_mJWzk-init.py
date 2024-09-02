"""
Init
"""

from yoyo import step

__depends__ = {}


steps = [
    step("""insert into admin(name) values('a1')""", "delete from admin"),
    step("""insert into admin(name) values('a2')""", "delete from admin"),
    step("""insert into admin(name) values('a3')""", "delete from admin"),
]
