# db.py
from sqlmodel import SQLModel, create_engine, Session, select, col
from models.hero import Hero
from models.team import Team

sqlite_file_name = "sqliteDb/database.db"  # this notation works
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)


def create_heroes_a():  # the amount of print statements is to make it easier
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


# end of create_heroes_a()

def create_heroes_b():
    with Session(engine) as session:
        # Instantiate the teams
        team_preventers = Team(name="Preventers", headquarters="Sharp Tower")
        team_z_force = Team(name="Z-Force", headquarters="Sister Margaret’s Bar")
        # Add the teams to the session
        session.add(team_preventers)
        session.add(team_z_force)
        # Commit the teams to the database
        session.commit()

        # Refresh the teams to get make sure the latest data is available in memory
        session.refresh(team_preventers)
        session.refresh(team_z_force)

        # Instantiate the heroes
        hero_deadpond = Hero(
            name="Deadpond", secret_name="Dive Wilson", team_id=team_z_force.id
        )
        hero_rusty_man = Hero(
            name="Rusty-Man",
            secret_name="Tommy Sharp",
            age=48,
            team_id=team_preventers.id,
        )
        hero_spider_boy = Hero(
            name="Spider-Boy",
            secret_name="Pedro Parqueador"
        )

        # Add our heroes to the session
        session.add(hero_deadpond)
        session.add(hero_rusty_man)
        session.add(hero_spider_boy)

        # Commit the heroes to the database
        session.commit()

        # Refresh the heroes to get make sure the latest data is available in memory
        session.refresh(hero_deadpond)
        session.refresh(hero_rusty_man)
        session.refresh(hero_spider_boy)
        print("Created hero:", hero_deadpond)
        print("Created hero:", hero_rusty_man)
        print("Created hero:", hero_spider_boy)
        print("")
        print("")


# end of create_heroes_b()

def select_heroes_a():
    with Session(engine) as session:  # This is one session above; it's a separate session
        statement = select(Hero).where(
            (col(Hero.age) <= 35) | (col(Hero.age) > 90)
        )  # returns Select OR SelectOfScalar
        results = session.exec(statement)  # returns Result OR ScalarResult
        heroes = results.all()
        print(heroes)
        print("")
        print("")


# end of select_heroes_a()

def select_heroes_b():
    with Session(engine) as session:
        statement = select(Hero, Team).where(Hero.team_id == Team.id)  # where team_id = Team.id
        results = session.exec(statement)
        for hero, team in results:
            print("Hero:", hero, "Team:", team)
    print("")
    print("")


# end of select_heroes_b()

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

def select_where_limit_heroes():
    with Session(engine) as session:
        statement = select(Hero).where(Hero.age > 32).limit(3)
        results = session.exec(statement)
        heroes = results.all()
        print(heroes)
        print("")
        print("")


# end of select_where_limit_heroes()

def update_heroes():
    with Session(engine) as session:
        statement = select(Hero).where(Hero.name == "Spider-Boy")
        results = session.exec(statement)
        hero = results.one()  # this looks like a safe guard, to get only the one record you seek back
        print("Hero:", hero)

        hero.age = 16
        session.add(hero)
        session.commit()
        session.refresh(hero)  # Because we refreshed it right after updating it,
        # it has fresh data, including the new age we just updated.
        print("Updated hero:", hero)
        print("")
        print("")


# end of update_heroes()

def update_multiple_heroes():
    with Session(engine) as session:
        # First I get this guy.
        statement = select(Hero).where(Hero.name == "Spider-Boy")
        results = session.exec(statement)
        hero_1 = results.one()
        print("Hero 1:", hero_1)

        # Then I get this guy.
        statement = select(Hero).where(Hero.name == "Captain North America")
        results = session.exec(statement)
        hero_2 = results.one()
        print("Hero 2:", hero_2)

        # Then I mutate this guy in memory.
        hero_1.age = 16
        hero_1.name = "Spider-Youngster"
        session.add(hero_1)

        # Then I mutate this guy in memory.
        hero_2.name = "Captain North America Except Canada"
        hero_2.age = 110
        session.add(hero_2)

        # Then I commit the changes to the database.
        session.commit()

        # Then I refresh explicitly to get the latest data from the database.
        session.refresh(hero_1)
        session.refresh(hero_2)

        # Then I print the updated data.
        print("Updated hero 1:", hero_1)
        print("Updated hero 2:", hero_2)
        print("")
        print("")


# end of update_multiple_heroes()

def delete_heroes():
    with Session(engine) as session:
        # Pull this guy into memory.
        statement = select(Hero).where(Hero.name == "Spider-Youngster")
        results = session.exec(statement)
        hero = results.one()
        print("Hero: ", hero)

        # Delete him from the database.
        session.delete(hero)
        # Commit the delete.
        session.commit()

        print("Deleted hero:", hero)

        # Now we try to pull that guy back into memory but we should get None.
        statement = select(Hero).where(Hero.name == "Spider-Youngster")
        results = session.exec(statement)
        hero = results.first()

        # Do the None check.
        if hero is None:
            print("There's no hero named Spider-Youngster")

    print("")
    print("")

# end of delete_heroes()
