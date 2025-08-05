from typing import Annotated
from datetime import datetime
from typing import Optional


from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select


class Transactions(SQLModel, table=True):
    __tablename__ = "transactions"  # nome seguro

    id: Optional[int] = Field(default=None, primary_key=True)
    value: float
    dataHora: datetime = Field(default_factory=datetime.utcnow)


postgres_url = ""
engine = create_engine(postgres_url, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
