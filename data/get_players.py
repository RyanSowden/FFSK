from sleeper_wrapper import League
from sleeper_wrapper import Players
from sleeper_wrapper import Stats
import pandas as pd


players = Players()
nfl_stats = players.get_all_players()
df = pd.DataFrame.from_dict(nfl_stats)
df.to_pickle('nfltest')
df = pd.read_pickle('nfltest')
result = df.transpose()
players = result[['player_id','full_name','position','team']]
players.to_csv('player_names.csv', index=False)

print('Players successfully updated')
