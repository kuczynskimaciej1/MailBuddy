import sqlite3
from DataSources.sqliteOperations import *

dbName = "localSqLite.db"

createDatabase(dbName)

con = sqlite3.connect(dbName)
cur = con.cursor()

# from models import Contact

# insertContact(Contact(first_name="Adam", last_name="Adamski", email="adamski.a@adamski.ad"))

# contacts = getContacts()

# [print(x) for x in contacts]

res = cur.execute("SELECT name FROM sqlite_master")
print(res.fetchall())