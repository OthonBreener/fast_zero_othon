from typing import Iterator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, registry

from fast_zero.settings import Settings

table_registry = registry()

engine = create_engine(Settings().DATABASE_URL)


# table_registry.metadata.create_all(engine)


# o comentário pragma: no cover, diz para o coverage não verificar essa função
def get_session() -> Iterator[Session]:  # pragma: no cover
    with Session(engine) as session:
        yield session
