import psycopg2
from config import load_config
from commands import matches,match_teams,events

test = "SELECT * FROM matches;"

def generate_db():

    config = load_config()
    creator = """CREATE TABLE matches (
        match_id INTEGER PRIMARY KEY,
        tournament_season VARCHAR(255) NOT NULL,
        date DATE NOT NULL,
        home_side VARCHAR(255) NOT NULL,
        away_side VARCHAR(255) NOT NULL,
        home_score VARCHAR(255) NOT NULL,
        away_score VARCHAR(255) NOT NULL
        );
        \n

        CREATE TABLE match_teams (
        match_id INTEGER NOT NULL,
        team VARCHAR NOT NULL,
        PRIMARY KEY (match_id, team),
        FOREIGN KEY (match_id) REFERENCES matches(match_id)
        );
        \n

        CREATE TABLE events (
        event_id INTEGER PRIMARY KEY,
        match_id INTEGER NOT NULL,
        team VARCHAR(255) NOT NULL,
        FOREIGN KEY (match_id, team) REFERENCES match_teams(match_id, team),
        type_name VARCHAR(255) NOT NULL,
        time FLOAT NOT NULL,
        progression_id INTEGER,
        x_start INTEGER,
        y_start INTEGER,
        x_end INTEGER,
        y_end INTEGER
        );\n
        
        CREATE TABLE progressions (
        progression_id INTEGER PRIMARY KEY,
        match_id INTEGER NOT NULL,
        team VARCHAR(255) NOT NULL,
        FOREIGN KEY (match_id, team) REFERENCES match_teams(match_id, team));"""

    destructor = "DROP TABLE matches,match_teams,events,progressions;"

    event_destructor = "DROP TABLE events"

    event_creator = """CREATE TABLE events (
            event_id INTEGER PRIMARY KEY,
            match_id INTEGER NOT NULL,
            team VARCHAR(255) NOT NULL,
            FOREIGN KEY (match_id, team) REFERENCES match_teams(match_id, team),
            type_name VARCHAR(255) NOT NULL,
            time FLOAT NOT NULL,
            progression_id INTEGER,
            half_id INTEGER,
            x_start INTEGER,
            y_start INTEGER,
            x_end INTEGER,
            y_end INTEGER
            );"""

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:

                def execute(sql):
                    cur.execute(sql)

                    if cur.description is not None:
                        if cur.rowcount <= 10:
                            print(cur.fetchall())
                        else:
                            print(cur.fetchmany(10))
                        print("\n")
                    
                #cur.execute(destructor)
                #cur.execute(creator)
                cur.execute(event_destructor)
                cur.execute(event_creator)
                #for match in matches:
                    #execute(match)
                #for match_team in match_teams:
                    #execute(match_team)
                for event in events:
                    execute(event)

            conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

generate_db()