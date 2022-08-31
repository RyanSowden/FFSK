from sleeper_wrapper import League
from sleeper_wrapper import Players
from sleeper_wrapper import Stats
import pandas as pd
from db_connect import connection
from sqlalchemy import create_engine

players = Players()
nfl_stats = players.get_all_players()
players_df = pd.DataFrame.from_dict(nfl_stats)
players_df.to_pickle('nfltest')
player_df = pd.read_pickle('nfltest')
result = player_df.transpose()
players = result[['player_id','full_name','position','team']]
players.to_csv('player_names.csv', index=False)

df = pd.read_csv('player_names.csv')
df.dropna(subset=['team'], inplace=True)
df['full_name'].fillna(df['player_id'], inplace=True)
df.iloc[0] = ['0', 'No Player Started','','']

engine = create_engine('postgresql+psycopg2://{user}:{pw}@localhost/{db}'
        .format(user='test',
            pw='test',
            db='ffsk'))

df.to_sql('players',con=engine, if_exists = 'replace', index=False)

print("Successfully added players to the database")
