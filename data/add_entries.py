from db_connect import connection
import pandas as pd
import psycopg2
from sqlalchemy import create_engine

#c = connection.cursor() #Establishing the connection to the database
engine = create_engine('postgresql+psycopg2://{user}:{pw}@localhost/{db}'
        .format(user='test',
            pw='test',
            db='ffsk'))

stats = pd.read_csv('Sleeper_Player_Names_V2.csv')

df  = stats[['player_id','full_name','position','team']]

df.to_sql('players',con=engine, if_exists = 'append', index=False)






#c.execute("INSERT INTO players(player_id,full_name,position,team) VALUES(%s,%s,%s,%s)",(stats['player_id'],stats['full_name'],stats['position'],stats['team'],))


#c.execute("INSERT INTO players (player_id) VALUES(%s)",(player_stats_list,))
#c.execute("INSERT INTO players (full_name) VALUES(%s)",(player_name_list,))
#c.execute("INSERT INTO players (position) VALUES(%s)",(position,))
#c.execute("INSERT INTO players (team) VALUES(%s)",(team,))

#connection.commit()# commiting the table to the database
#c.close() # closing the conneciton - very important
