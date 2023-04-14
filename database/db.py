# db.py
from sqlmodel import SQLModel, create_engine, Session, select, col
from models.hero import Hero

# sqlite_file_name = "../sqliteDb/database.db" #this notation doesn't work
sqlite_file_name = "sqliteDb/database.db"  # this notation works
# sqlite_file_name = "/Users/gabe.cruz/wrk/s_tutorial/sqliteDb/database.db" #this notation works
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)


def create_heroes():  # the amount of print statements is to make it easier
    # to see what's going on
    hero_1 = Hero(name="Deadpond", secret_name="Dive Wilson")
    hero_2 = Hero(name="Spider-Boy", secret_name="Pedro Parqueador")
    hero_3 = Hero(name="Rusty-Man", secret_name="Tommy Sharp", age=48)
    hero_4 = Hero(name="Tarantula", secret_name="Natalia Roman-on", age=32)
    hero_5 = Hero(name="Black Lion", secret_name="Trevor Challa", age=35)
    hero_6 = Hero(name="Dr. Weird", secret_name="Steve Weird", age=36)
    hero_7 = Hero(name="Captain North America", secret_name="Esteban Rogelios", age=93)

    print("")
    print("")
    print("Before interacting with the database")
    print("Hero 1:", hero_1)
    print("Hero 2:", hero_2)
    print("Hero 3:", hero_3)
    print("")
    print("")

    with Session(engine) as session:  # this is one session below it's a separate session
        session.add(hero_1)
        session.add(hero_2)
        session.add(hero_3)
        session.add(hero_4)
        session.add(hero_5)
        session.add(hero_6)
        session.add(hero_7)
        print("")
        print("")
        session.commit()
        print("")
        print("")

        print("")
        print("")
        print("After committing the session")
        print("Hero 1:", hero_1)
        print("Hero 2:", hero_2)
        print("Hero 3:", hero_3)
        print("")
        print("")

        print("")
        print("")
        print("After committing the session, show IDs")
        print("Hero 1 ID:", hero_1.id)
        print("Hero 2 ID:", hero_2.id)
        print("Hero 3 ID:", hero_3.id)
        print("")
        print("")

        print("")
        print("")
        print("After committing the session, show names")
        print("Hero 1 name:", hero_1.name)
        print("Hero 2 name:", hero_2.name)
        print("Hero 3 name:", hero_3.name)

        print("")
        print("")
        session.refresh(hero_1)
        session.refresh(hero_2)
        session.refresh(hero_3)
        print("")
        print("")

        print("")
        print("")
        print("After refreshing the heroes")
        print("Hero 1:", hero_1)
        print("Hero 2:", hero_2)
        print("Hero 3:", hero_3)
    #   session closes here because it comes out of the with block
    print("")
    print("")
    print("After the session closes")
    print("Hero 1:", hero_1)
    print("Hero 2:", hero_2)
    print("Hero 3:", hero_3)
    print("")
    print("")


# end of create_heroes()

def select_heroes():
    with Session(engine) as session:  # This is one session above; it's a separate session
        statement = select(Hero).where(
            (col(Hero.age) <= 35) | (col(Hero.age) > 90)
        )  # returns Select OR SelectOfScalar
        results = session.exec(statement)  # returns Result OR ScalarResult
        heroes = results.all()
        print(heroes)
        print("")
        print("")


# end of select_heroes()
def select_first_hero():
    with Session(engine) as session:  # This is also a different session.
        statement = select(Hero).where(
            (col(Hero.age) <= 25)
        )  # returns Select OR SelectOfScalar
        results = session.exec(statement)  # returns Result OR ScalarResult
        hero = results.first()
        print("Hero:", hero)
        print("")
        print("")


# end of select_first_hero()

def select_exactly_one_hero():
    with Session(engine) as session:  # This is also a different session.
        statement = select(Hero).where(
            (col(Hero.name) == "Deadpond")
        )  # returns Select OR SelectOfScalar
        results = session.exec(statement)  # returns Result OR ScalarResult
        hero = results.one()
        print("Hero:", hero)
        print("")
        print("")


# end of select_exactly_one_hero()

def select_one_hero_inline():
    with Session(engine) as session:  # This is also a different session.
        hero = session.exec(select(Hero).where(col(Hero.name) == "Deadpond")).one()
        print("Hero:", hero)
        print("")
        print("")


# end of select_one_hero_inline()


def select_first_hero_inline():
    with Session(engine) as session:  # This is also a different session.
        hero = session.exec(select(Hero).where((col(Hero.age) <= 35) | (col(Hero.age) > 90))).first()
        print("Hero:", hero)
        print("")
        print("")


# end of select_first_hero_inline()

def select_first_first_heroes():
    with Session(engine) as session:
        statement = select(Hero).where(Hero.id == 1)  # first
        results = session.exec(statement)
        hero = results.first()  # first
        print("Hero:", hero)
        print("")
        print("")


# end of select_first_first_heroes()

def select_with_heroes_pk_direct():
    with Session(engine) as session:
        hero = session.get(Hero, 1)  # shortcut, no select being used
        print("Hero:", hero)
        print("")
        print("")


# end of select_with_heroes_pk_direct()

def select_with_heroes_pk_direct_no_data():
    with Session(engine) as session:
        hero = session.get(Hero, 9001)  # no data because the id is not in the table
        print("Hero:", hero)
        print("")
        print("")


# end of select_with_heroes_pk_direct_no_data()

def select_limited_heroes(limit=1):
    with Session(engine) as session:
        statement = select(Hero).limit(limit)
        results = session.exec(statement)
        heroes = results.all()
        print(heroes)
        print("")
        print("")


# end of select_limited_heroes()

def select_limited_with_offset_heroes():
    with Session(engine) as session:
        statement = select(Hero).offset(3).limit(3)
        results = session.exec(statement)
        heroes = results.all()
        print(heroes)
        print("")
        print("")


# end of select_limited_with_offset_heroes()

def select_next_batch_of_heroes():
    with Session(engine) as session:
        statement = select(Hero).offset(6).limit(3)  # Then to get the next batch of 3 rows we would offset
        # all the ones we already saw, the first 6:
        # Basically, skip the next 6 rows and then get the next 3 rows
        # This assumes that we displayed the first 6 in another method call.
        # The user is done with those and is moving on to the next 3
        # In this current database, there are only 7, so we call the next 3, we only get the 1 back.
        results = session.exec(statement)
        heroes = results.all()
        print(heroes)
        print("")
        print("")
# end of select_next_batch_of_heroes()
