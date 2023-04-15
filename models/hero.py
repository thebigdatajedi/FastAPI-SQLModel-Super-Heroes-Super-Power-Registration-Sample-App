from typing import Optional

from sqlmodel import Field, SQLModel, create_engine


class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    secret_name: str
    age: Optional[int] = Field(default=None, index=True)
    team_id: Optional[int] = Field(default=None, foreign_key="team.id")  # Using SQLModel, in most of the cases
    # you only need a field (column) with a foreign_key in the Field() with a string pointing to another table
    # and column to connect two tables.
    # NOTE::...with a string pointing to another table and column to connect the two tables!!!
