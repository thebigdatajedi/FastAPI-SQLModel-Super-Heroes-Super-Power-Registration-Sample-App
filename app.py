# app.py
from database.db import engine, SQLModel, create_heroes, select_heroes, select_first_hero, select_exactly_one_hero, \
    select_one_hero_inline, select_first_hero_inline, select_with_heroes_pk_direct, select_first_first_heroes, \
    select_with_heroes_pk_direct_no_data, select_limited_heroes, select_limited_with_offset_heroes, \
    select_next_batch_of_heroes
import os


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def clean_up_db():  # Adding this so the db file can be cleaned
    # up before each run and the ids can stay 1, 2, 3. Like the example in the tutorial.
    db = "sqliteDb/database.db"

    if os.path.exists(db):
        os.remove(db)


def main():
    clean_up_db()
    create_db_and_tables()
    create_heroes()
    select_heroes()
    select_first_hero()
    select_exactly_one_hero()
    select_one_hero_inline()
    select_first_hero_inline()
    select_first_first_heroes()
    select_with_heroes_pk_direct()
    select_with_heroes_pk_direct_no_data()
    select_limited_heroes(5)
    select_limited_with_offset_heroes()
    select_next_batch_of_heroes()


if __name__ == "__main__":
    main()
