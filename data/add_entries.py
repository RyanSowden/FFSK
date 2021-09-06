from db_connect import connection
import pandas as pd
import psycopg2
from sqlalchemy import create_engine

engine = create_engine('postgresql+psycopg2://{user}:{pw}@localhost/{db}'
        .format(user='test',
            pw='test',
            db='ffsk'))

stats = pd.read_csv('player_names.csv')

df  = stats[['player_id','full_name','position','team']]

df.to_sql('players',con=engine, if_exists = 'replace', index=False)

print("Successfully added players to the database")







