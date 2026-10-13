import pandas as pd
from socceraction.data.wyscout import PublicWyscoutLoader

loader = PublicWyscoutLoader(root="./data/wyscout")

team_names = {}
goals = {}

df_matches = loader.games(season_id=181150, competition_id=364)
df_events = pd.DataFrame()
i = 0
for game_id in df_matches["game_id"]:
    teams = loader.teams(game_id)
    events = loader.events(game_id)
    is_goal = events["tags"].apply(lambda tags: any(tag.get('id') == 101 for tag in tags))

    is_og = events["tags"].apply(lambda tags: any(tag.get('id') == 102 for tag in tags))

    is_goal_event = events["type_id"].isin([3,8,10])

    goals_for = is_goal & is_goal_event

    own_goals_for = is_og

    for _, team in teams.iterrows():
        team_names[team["team_id"]] = team["team_name"]

        normal_goals = (
            goals_for
            & (events["team_id"] == team["team_id"])
        )

        own_goals = (
            own_goals_for
            & (events["team_id"] != team["team_id"])
        )

        goals[(game_id, team["team_id"])] = (own_goals | normal_goals).sum()

    valid_types = events["type_id"].isin([1,2,3,5,6,8,10])

    valid_events = events.loc[valid_types].copy()

    team_change = valid_events["team_id"].ne(valid_events["team_id"].shift())

    ends_progression = valid_events["type_id"].isin([2,5,6])

    new_progression = (
    team_change
    | ends_progression.shift(fill_value=False)
    )

    valid_events["progression"] = (
        new_progression.cumsum() - 1
    )
        
    events["progression"] = pd.NA
    events.loc[valid_events.index, "progression"] = valid_events["progression"]
    df_events = pd.concat([df_events,events], axis=0)
            
df_matches["home_team_name"] = df_matches["home_team_id"].map(team_names)
df_matches["away_team_name"] = df_matches["away_team_id"].map(team_names)
df_matches["home_team_goals"] = df_matches.apply(
    lambda row: goals.get(
        (row["game_id"], row["home_team_id"]),
        -1
    ),
axis = 1
)
df_matches["away_team_goals"] = df_matches.apply(
    lambda row: goals.get(
        (row["game_id"], row["away_team_id"]),
        -1
    ),
axis = 1
)
            
df_events["team"] = df_events["team_id"].map(team_names)

matches = (
    "INSERT INTO matches(match_id, tournament_season, date, home_side, away_side, home_score, away_score) VALUES "
    + "("
    + df_matches["game_id"].astype(str)
    + ", '2017-18 Premier League', '"
    + df_matches["game_date"].dt.date.astype(str)
    + "', '"
    + df_matches["home_team_name"].astype(str)
    + "', '"
    + df_matches["away_team_name"].astype(str)
    + "', '"
    + df_matches["home_team_goals"].astype(str)
    +  "', '"
    + df_matches["away_team_goals"].astype(str)
    + "');"
)

match_teams = (
    "INSERT INTO match_teams(match_id, team) VALUES"
    + "("
    + df_matches["game_id"].astype(str)
    + ", '"
    + df_matches["home_team_name"].astype(str)
    + "'), ("
    + df_matches["game_id"].astype(str)
    + ", '"
    + df_matches["away_team_name"].astype(str)
    + "');"
)

events = (
    "INSERT INTO events(event_id, match_id, team, type_name, time, progression_id, half_id, x_start, y_start, x_end, y_end) VALUES"
    + "( "
    + df_events["event_id"].astype(str)
    + ", "
    + df_events["game_id"].astype(str)
    + ", '"
    + df_events["team"].astype(str)
    + "', '"
    + df_events["type_name"].astype(str)
    + "', "
    + df_events["milliseconds"].round().astype(str)
    + ", "
    + df_events["progression"].apply(
    lambda x: "NULL" if pd.isna(x) else str(x)
)
    + ", "
    + df_events["period_id"].astype(str)
    + ", "
    + df_events["positions"].str[0].str['x'].apply(
    lambda x: "NULL" if pd.isna(x) else str(x)
)
    + ", "
    + df_events["positions"].str[0].str['y'].apply(
    lambda x: "NULL" if pd.isna(x) else str(x)
)
    + ", "
    + df_events["positions"].str[1].str['x'].apply(
    lambda x: "NULL" if pd.isna(x) else str(x)
)
    + ", "
    + df_events["positions"].str[1].str['y'].apply(
    lambda x: "NULL" if pd.isna(x) else str(x)
)
    + ");")