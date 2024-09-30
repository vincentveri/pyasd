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

    with open('persone.csv', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter="\t")
        for idx, row in enumerate(reader, start=1):
            if row[9]:
                datanascita = datetime.strptime(row[9], "%d/%m/%Y").strftime("%Y-%m-%d")
            else:
                datanascita = None
            if row[11]:
                datarilasciotessera = datetime.strptime(row[11], "%d/%m/%Y").strftime("%Y-%m-%d")
            else:
                datarilasciotessera = None
            person = (idx, row[2], row[1], row[20], datanascita, row[10], None, row[8], 'CSI Terra d\'Otranto', row[0], datarilasciotessera,
                      row[6], row[5], None, row[7], row[14], None)
            people.append(person)

    cur.executemany("INSERT INTO people VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", people)

    con.commit()

