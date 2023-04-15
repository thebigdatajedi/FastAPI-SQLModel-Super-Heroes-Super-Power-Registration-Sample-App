# app.py
from database.db import engine, SQLModel, create_heroes_b, select_heroes_left_outer_join, \
    select_heroes_left_outer_join_with_results_all
import os


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
    print("")
    print("")


def clean_up_db():  # Adding this so the db file can be cleaned
    # up before each run and the ids can stay 1, 2, 3. Like the example in the tutorial.
    db = "sqliteDb/database.db"

    if os.path.exists(db):
        os.remove(db)


def main():
    clean_up_db()
    create_db_and_tables()
    create_heroes_b()
    select_heroes_left_outer_join()
    select_heroes_left_outer_join_with_results_all()


if __name__ == "__main__":
    main()
