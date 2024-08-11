from typing import Annotated, Generator, Any

from fastapi import Depends
from sqlalchemy.orm import Session

from .common import engine


def _get_session() -> Generator:
    with Session(engine) as s:
        with s.begin():
            yield s


SessionDep = Annotated[Session, Depends(_get_session)]
