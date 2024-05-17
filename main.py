from argparse import ArgumentParser
from typing import TYPE_CHECKING, Optional


from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel, Field, Relationship

# PostgreSQL connection URL
DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost/sqlmodel_tutor"

# Create the async engine
async_engine = create_async_engine(
    DATABASE_URL,
    future=True,
    echo=True,
)

# Create async session class
async_session = sessionmaker(
    autocommit=False, autoflush=False, bind=async_engine, class_=AsyncSession
)

# Dependency to get async session
async def get_session():
    async with async_session() as session:
        yield session


# Many to one
class Item(SQLModel, table=True):
    __tablename__ = 'items'

    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    description: str = Field(index=True)
    owner_id: int | None = Field(default=None, foreign_key='users.id', nullable=False)

    # Here need to use `Optional['User']` , `'User'`` is not work
    # https://sqlmodel.tiangolo.com/tutorial/code-structure/#make-circular-imports-work
    owner: Optional['User'] = Relationship(back_populates="items")

# Many to many
class UserStockLink(SQLModel, table=True):
    user_id: int | None = Field(default=None, foreign_key='users.id', primary_key=True)
    stock_id: int | None = Field(default=None, foreign_key='stocks.id', primary_key=True)


class User(SQLModel, table=True):
    __tablename__ = 'users'

    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True)
    age: int | None = Field(default=None)
    hashed_password: str
    is_active: bool = Field(default=True)

    items: list['Item'] = Relationship(back_populates='owner')
    stocks: list['Stock'] = Relationship(back_populates='users', link_model=UserStockLink)


class Stock(SQLModel, table=True):
    __tablename__ = 'stocks'

    id: int | None = Field(default=None, primary_key=True)
    stock_id: str = Field(index=True, unique=True)
    name: str = Field(index=True, unique=True)

    users: list['User'] = Relationship(back_populates='stocks', link_model=UserStockLink)


app = FastAPI()


async def init_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)
        print('Finish initial DB!')

# Route to create a new item
@app.post("/items/")
async def create_item(item: Item, session: AsyncSession = Depends(get_session)):
    # async with session.begin():
    session.add(item)
    await session.commit()
    await session.refresh(item)
    return item

@app.post("/users/")
async def create_item(user: User, session: AsyncSession = Depends(get_session)):
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user

if __name__ == '__main__':
    parser = ArgumentParser(description='SQLModel Tutor')
    parser.add_argument('init-db', help='Initial DB')

    if parser.parse_args(['init-db']):
        import asyncio

        asyncio.run(init_db())
