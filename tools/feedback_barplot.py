import os
from collections import Counter
from urllib.parse import urlparse

import psycopg2

import matplotlib.pyplot as plt


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
    cursor.execute("""SELECT * FROM Feedback""")
    values = [o[1] for o in cursor.fetchall()]
    counter = Counter(values)

    plt.bar(['ok', 'meh', 'bad'], 
            [counter['ok'], counter['meh'], counter['bad']],
            color=('g', 'y', 'r'),
            edgecolor='black', 
            linewidth=2,
            tick_label=['Well Classified', 'Not Sure', 'Wrong'])

    plt.title('Feedback gathered - OPTCbx')

    for k, v in counter.items():
        plt.text(x=k, y=v + 5, s=f'#{v}', size=10)

    plt.show()

except psycopg2.Error as error:
    print(error)
    print ("Error while connecting to PostgreSQL", error)
finally:
    if connection:
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")