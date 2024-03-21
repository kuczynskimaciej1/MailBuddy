import pytest
from models import *
from DataSources.dataSources import DatabaseHandler
from models import Contact

@pytest.fixture


insertContact(Contact(first_name="Adam", last_name="Adamski", email="adamski.a@adamski.ad"))
# contacts = getContacts()
# [print(x) for x in contacts]

con = sqlite3.connect(dbName)
cur = con.cursor()
result = cur.execute("SELECT first_name, last_name, email from Contacts")
print(result.fetchall())