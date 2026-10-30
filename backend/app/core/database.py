from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.core.config import settings

engine = create_engine(settings.database_url, echo=True)


def get_db() -> Generator[Session]:
    with Session(engine) as session:
        yield session
