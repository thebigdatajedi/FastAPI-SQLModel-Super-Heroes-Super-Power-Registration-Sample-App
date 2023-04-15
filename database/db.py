# db.py
from sqlmodel import SQLModel, create_engine, Session, select, col
from models.hero import Hero
from models.team import Team

sqlite_file_name = "sqliteDb/database.db"  # this notation works
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)


def create_heroes():
    with Session(engine) as session:
        # Instantiate the teams
        team_preventers = create_team("Preventers", "Sharp Tower")
        team_z_force = create_team("Z-Force", "Sister Margaret’s Bar")
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

        # Add a connection with team - Update Operation
        hero_spider_boy.team_id = team_preventers.id
        session.add(hero_spider_boy)
        session.commit()
        session.refresh(hero_spider_boy)
        print("Updated hero:", hero_spider_boy)

        # Remove a connection with team - Update Operation
        hero_spider_boy.team_id = None
        session.add(hero_spider_boy)
        session.commit()
        session.refresh(hero_spider_boy)
        print("No longer Preventer:", hero_spider_boy)
    print("")
    print("")


# end of create_heroes()

def create_team(team_name: str, team_headquarters: str):
    team = Team(name=team_name, headquarters=team_headquarters)
    return team


# end of create_heroes_c()
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

def select_heroes_with_join():
    with Session(engine) as session:
        statement = select(Hero, Team).join(Team)  # on keyword is implied
        results = session.exec(statement)
        for hero, team in results:
            print("Hero:", hero, "Team:", team)
    print("")
    print("")


# end of select_heroes_with_join()

def select_heroes_left_outer_join():
    with Session(engine) as session:
        statement = select(Hero, Team).join(Team, isouter=True)  # join Team isouter=True, Hero is the left table
        # and I'm joining the records that don't meet the criteria thus they are out or outer
        results = session.exec(statement)
        for hero, team in results:
            print("Hero:", hero, "Team:", team)
    print("")
    print("")


# end of select_heroes_left_outer_join()

def select_heroes_left_outer_join_with_results_all():
    with Session(engine) as session:
        statement = select(Hero, Team).join(Team, isouter=True)  # join Team isouter=True, Hero is the left table
        # and I'm joining the records that don't meet the criteria thus they are out or outer
        results = session.exec(statement).all()
        print(results)
    print("")
    print("")


# end of select_heroes_left_outer_join_with_results_all()

def select_on_heroes_only_still_join_on_team_where_team_name():
    with Session(engine) as session:
        statement = select(Hero).join(Team).where(Team.name == "Preventers")  # dont include the Team data in the
        # result but join (filter) on Team.name.
        results = session.exec(statement)
        for hero in results:
            print("Preventer Hero:", hero)
    print("")
    print("")


# end of select_on_heroes_only_still_join_on_team_where_team_name()

def select_on_heroes_only_still_join_on_team_where_team_name_results_all():
    with Session(engine) as session:
        statement = select(Hero).join(Team).where(Team.name == "Preventers")  # dont include the Team data in the
        # result but join (filter) on Team.name.
        results = session.exec(statement).all()
        print(results)
    print("")
    print("")


# end of select_on_heroes_only_still_join_on_team_where_team_name_results_all()

def select_heroes_and_team_join_on_team_where_team_name():
    with Session(engine) as session:
        statement = select(Hero, Team).join(Team).where(Team.name == "Preventers")  # join on Team
        # where Team.name
        results = session.exec(statement)
        for hero, team in results:
            print("Preventer Hero:", hero, "Team:", team)
    print("")
    print("")


# end of select_heroes_and_team_join_on_team_where_team_name()

def select_heroes_and_team_join_on_team_where_team_name_results_all():
    with Session(engine) as session:
        statement = select(Hero, Team).join(Team).where(Team.name == "Preventers")  # join on Team
        # where Team.name
        results = session.exec(statement).all()
        print(results)
    print("")
    print("")


# end of select_heroes_and_team_join_on_team_where_team_name_results_all()

def select_heroes_and_team_without_join_on_team_where_team_name():
    with Session(engine) as session:
        statement = select(Hero, Team).where(Team.name == "Preventers")  # join on Team
        # where Team.name
        results = session.exec(statement)
        for hero, team in results:
            print("Preventer Hero:", hero, "Team:", team)
    print("")
    print("")


# end of select_heroes_and_team_without_join_on_team_where_team_name()

def select_heroes_and_team_without_join_on_team_where_team_name_results_all():
    with Session(engine) as session:
        statement = select(Hero, Team).where(Team.name == "Preventers")  # join on Team
        # where Team.name
        results = session.exec(statement).all()
        print(results)
    print("")
    print("")


# end of select_heroes_and_team_without_join_on_team_where_team_name_results_all()


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
