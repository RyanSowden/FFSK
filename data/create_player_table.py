from db_connect import connection

c = connection.cursor() #Establishing the connection to the database

c.execute(
        '''CREATE TABLE IF NOT EXISTS players
        (id SERIAL PRIMARY KEY, player_id varchar, full_name text , position text , team text)'''
        )

print('Table successfully created')


connection.commit()# commiting the table to the database
c.close() # closing the conneciton - very important
