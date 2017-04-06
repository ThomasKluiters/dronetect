import os
import sqlite3
import sys

try:
    BASE_DIR = sys.argv[1]
except:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_location = os.path.join(BASE_DIR, 'data.db')

conn = sqlite3.connect(db_location)
c = conn.cursor()

rows = c.execute('SELECT * FROM ' + sys.argv[2])

for row in rows:
    print row
