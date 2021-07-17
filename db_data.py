from db_connect import connection

c = connection.cursor() #Establishing the connection to the database

c.execute(
        '''CREATE TABLE IF NOT EXISTS league
        (id SERIAL PRIMARY KEY, league_name text, league_number integer)'''
        )

connection.commit()# commiting the table to the database
c.close() # closing the conneciton - very important
