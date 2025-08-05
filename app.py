from fastapi import Depends, FastAPI, HTTPException, Query
from db import *
from typing import Annotated
from sqlmodel import select
from datetime import datetime, timezone
from fastapi.responses import JSONResponse


async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield
    print("app shutting down")


app = FastAPI(lifespan=lifespan)


@app.get("/transactions", response_model=list[Transactions])
def get_all_transactions(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[Transactions]:
    transactions = session.exec(select(Transactions)).all()
    return transactions


@app.post("/transactions", response_model=Transactions)
def add_transaction(transaction: Transactions, session: SessionDep):
    dataHora = datetime.fromisoformat(transaction.dataHora)
    if dataHora > datetime.now(timezone.utc):
        raise HTTPException(status_code=400, detail="dataHora can`t be in the future!")
    else:
        session.add(transaction)
        session.commit()
        return JSONResponse(
            status_code=200,
            content={
                "message": "Transaction added successfully!",
                "transaction": transaction.model_dump_json(),
            },
        )
