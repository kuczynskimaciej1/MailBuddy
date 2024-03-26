import pytest
import os
import sqlite3
from models import *
from DataSources.sqliteOperations import sqlite
from DataSources.dataSources import DatabaseHandler


localDbName = "localSQLite.sqlite3"
insertCommand = "INSERT INTO Contacts (first_name, last_name, email) VALUES (?, ?, ?)"
selectCommand = "SELECT email, first_name, last_name from Contacts where email = ?"

@pytest.fixture
def contact1() -> Contact:
    return Contact("Adam", "Adamski", "adamski.a@aa.aa") # Contact("Wojciech", "Wojciechowski", "ww@ww.ww")]
    
@pytest.fixture
def sqliteConnection() -> sqlite3.Connection:
    return sqlite3.connect(localDbName)

@pytest.fixture
def dropDatabase() -> bool:
    if os.path.exists(localDbName):
        os.remove(path=localDbName)
        return True
    return False
        
@pytest.fixture
def createDatabase() -> bool:
    testHandler = sqlite(localDbName)
    testHandler.createDatabase([Contact])
    return True
    
@pytest.fixture
def recreateDatabase(dropDatabase, createDatabase)-> bool:
    return dropDatabase and createDatabase

def test_contact_sqlite_insertable(recreateDatabase, contact1, sqliteConnection):
    c = contact1
    parameters = (c.first_name, c.last_name, c.email)
    
    sqliteConnection.cursor().execute(insertCommand, parameters)
    sqliteConnection.commit()
    
    scur = sqliteConnection.cursor().execute(selectCommand, (c.email, ))
    selectionResult = scur.fetchall()
    print(selectionResult)
    assert len(selectionResult) == 1, f"output: {selectionResult}, got {len(selectionResult)}"
    assert selectionResult[0][0] == c.email, f"output: {selectionResult[0]}"
    

# def contact_sqlite_pk_unique_email():
    