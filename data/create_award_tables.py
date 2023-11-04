
from db_connect import connection

c = connection.cursor() #Establishing the connection to the database

c.execute(
        '''CREATE TABLE IF NOT EXISTS standings
        (id SERIAL PRIMARY KEY, user_name varchar, pf numeric , pa numeric,league varchar, record varchar)'''
        )

c.execute(
        '''CREATE TABLE IF NOT EXISTS week1
        (id SERIAL PRIMARY KEY, league varchar, user_name varchar, pf numeric , pa numeric)'''
        )

c.execute(
        '''CREATE TABLE IF NOT EXISTS week2
        (id SERIAL PRIMARY KEY, league varchar, user_name varchar, pf numeric , pa numeric)'''
        )

c.execute(
        '''CREATE TABLE IF NOT EXISTS week3
        (id SERIAL PRIMARY KEY, league varchar, user_name varchar, pf numeric , pa numeric)'''
        )



print('Tables successfully created')


connection.commit()# commiting the table to the database
c.close() # closing the conneciton - very important