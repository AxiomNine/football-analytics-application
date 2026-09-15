"""commands = ([
    \"""CREATE TABLE matches (
    match_id SERIAL PRIMARY KEY,
    tournament_season VARCHAR(255) NOT NULL,
    date DATE NOT NULL,
    home_side VARCHAR(255) NOT NULL,
    away_side VARCHAR(255) NOT NULL,
    home_score VARCHAR(255) NOT NULL,
    away_score VARCHAR(255) NOT NULL
    )\"""
])"""

import pandas as pd
from socceraction.data.wyscout import PublicWyscoutLoader

def load_pl():
    loader = PublicWyscoutLoader(root="./data/wyscout")

    df_matches = loader.games(season_id=181144, competition_id=795) 
    print(df_matches.head())

load_pl()
commands = ([
    """INSERT INTO matches(match_id, tournament_season, date, home_side, away_side, home_score, away_score)
    VALUES ()"""
])