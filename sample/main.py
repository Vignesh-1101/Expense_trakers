import string
from fastapi import FastAPI, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker
from sqlalchemy import String, create_engine
from pydantic import BaseModel
from models import Expense


app = FastAPI()

engine = create_engine("mysql://user:user@localhost:3307/expense_traker")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base = declarative_base()


def get_db():
    """
    This function is likely used to retrieve a database connection or handle.
    """
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_session():
    """
    This function is likely intended to retrieve a session for a user.
    """
    with Session(engine) as session:
        yield session


# This class likely represents a model for tracking expenses.
class Expenses(BaseModel):
    name: str
    amount: float
    category: str


# The `add_expenses` function is a POST endpoint in the FastAPI application that allows users to
# add new expenses to the expense tracker. It takes in a JSON payload containing the name, amount,
# and category of the expense to be added. The function then creates a new `Expense` object with
# the provided data, adds it to the database session, commits the transaction, and returns a
# success message if the expense is created successfully.
@app.post("/expenses")
def add_expenses(
    expense: Expenses, db: Session = Depends(get_session)
):
    expense = Expense(
        name=expense.name, amount=expense.amount, category=expense.category
    )
    db.add(expense)
    db.commit()
    return {"success": True, "message": "Created Successfully"}


# The `get_expenses` function is a GET endpoint in the FastAPI application that allows users to
# retrieve expenses from the expense tracker. It takes in an optional query parameter `Category`
# which filters the expenses based on the provided category.
@app.get("/expenses")
def get_expenses(db: Session = Depends(get_session), Category=Query(str)):
    query = db.query(Expense)
    if Category:
        query = query.filter(Expense.category == Category)
    expenses = query.all()
    return {"Success": True, "data": expenses}


# The `total` function is a GET endpoint in the FastAPI application that calculates the total sum
# of all expenses stored in the database.
@app.get("/totals")
def total(db: Session = Depends(get_session)):
    total_expense = 0
    expense = db.query(Expense.amount).all()
    for total in expense:
        total_expense += total[0]
    return {"success": True, "total": total_expense}
