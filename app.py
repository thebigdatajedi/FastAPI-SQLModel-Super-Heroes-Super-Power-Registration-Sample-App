# app.py
from database.db import engine, SQLModel

SQLModel.metadata.create_all(engine)
