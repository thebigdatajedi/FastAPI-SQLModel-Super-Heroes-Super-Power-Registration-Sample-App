# db.py
from sqlmodel import SQLModel, create_engine
from models.hero import Hero

# sqlite_file_name = "../sqliteDb/database.db" #this notation doesn't work
sqlite_file_name = "sqliteDb/database.db"  # this notation works
# sqlite_file_name = "/Users/gabe.cruz/wrk/s_tutorial/sqliteDb/database.db" #this notation works
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)
