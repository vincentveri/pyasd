import random
import sqlite3
from datetime import datetime

con = sqlite3.connect('pyasd.db')
cur = con.cursor()

if __name__ == '__main__':

    cur.execute("""
        DELETE FROM transactions
    """)

    data = []

    for idx in range(3, 1243):
        id_persona = random.randrange(1, 3)
        row = (idx, '2024-10-01', 'RANDOM', '100.00', None, None, id_persona)
        data.append(row)

    cur.executemany("INSERT INTO transactions VALUES(?,?,?,?,?,?,?)", data)

    con.commit()

