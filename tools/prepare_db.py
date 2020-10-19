import psycopg2
import os
from urllib.parse import urlparse

result = urlparse(os.environ['DATABASE_URL'])
username = result.username
password = result.password
database = result.path[1:]
hostname = result.hostname

try:
    connection = psycopg2.connect(
        database=database,
        user=username,
        password=password,
        host=hostname
    )

    cursor = connection.cursor()
    # # Create table statement
    create_table = "create table Feedback (id serial PRIMARY KEY, fb text)"
    drop_table = "DROP TABLE Feedback;"

    cursor.execute(drop_table)
    connection.commit()

    cursor.execute(create_table)
    connection.commit()

    cursor = connection.cursor()
    cursor.execute("""SELECT table_name FROM information_schema.tables
       WHERE table_schema = 'public'""")
    for table in cursor.fetchall():
        print(table)

except (Exception, psycopg2.Error) as error :
    print(error)
    print ("Error while connecting to PostgreSQL", error)
finally:
    #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")