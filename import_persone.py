import csv
import sqlite3
from datetime import datetime

con = sqlite3.connect('pyasd.db')
cur = con.cursor()

if __name__ == '__main__':

    cur.execute("""
        DELETE FROM people
    """)

    people = []

    with open('persone.csv') as file:
        reader = csv.reader(file, delimiter="\t")
        for idx, row in enumerate(reader, start=1):
            if row[9]:
                datanascita = datetime.strptime(row[9], "%d/%m/%Y").strftime("%Y-%m-%d")
            else:
                datanascita = None
            person = (idx, row[2], row[1], row[11], datanascita, row[10], None, row[8])
            people.append(person)

    cur.executemany("INSERT INTO people VALUES(?, ?, ?, ?, ?, ?, ?, ?)", people)

    con.commit()

