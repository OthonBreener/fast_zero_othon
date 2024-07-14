from typing import Iterator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, registry

from fast_zero.settings import Settings

table_registry = registry()

engine = create_engine(Settings().DATABASE_URL)

# table_registry.metadata.create_all(engine)


def get_session() -> Iterator[Session]:
    with Session(engine) as session:
        yield session
