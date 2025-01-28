from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import String, Column, Integer, Float
Base = declarative_base()

Base = declarative_base()
class Expense(Base):
    __tablename__ = 'expenses'
    # - `name` (string): Name of the expense.
    # - `amount` (float): Amount spent for the expense.
    # - `category` (string): Category to which the expense belongs.
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, index=True)
    amount = Column(Float)
    category = Column(String, default=False)
