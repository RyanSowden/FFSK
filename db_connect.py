import psycopg2

try:
    connection = psycopg2.connect(
            user='test',
            password='test',
            host = '127.0.0.1',
            port = '5432',
            database = 'ffsk')

    c = connection.cursor()

    print('Successfully connected to PostgreSQL')

except (Exception, psycopg2.Error) as error:
    print('Error while connectiong to PostgreSQL', error)






