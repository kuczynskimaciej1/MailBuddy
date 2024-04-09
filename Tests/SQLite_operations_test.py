import pytest
from time import sleep
import os
import sqlite3 # TODO to be changed into SQLAlchemy
from models import Contact
from dataGenerators import genContact
# from DataSources.sqliteOperations import sqlite
from DataSources.dataSources import DatabaseHandler


localDbName = "localSQLite.sqlite3"
dbURL = f"sqlite:///{localDbName}.db"

insertCommand = "INSERT INTO Contacts (first_name, last_name, email) VALUES (?, ?, ?)"
selectCommand = "SELECT email, first_name, last_name from Contacts where email = ?"

@pytest.fixture
def getDatabaseHandler(request) -> DatabaseHandler:
    return DatabaseHandler(dbURL, (request["table_classes"]))

@pytest.fixture
def dropDatabase() -> bool:
    if os.path.exists(localDbName):
        attempt = 0
        while(attempt < 5):
            try:
                os.remove(path=localDbName)
                return True
            except PermissionError:
                sleep(1)  #TODO Na pewno da się lepiej!
                attempt += 1
    return False

@pytest.fixture
def createDatabase(request) -> bool:
    getDatabaseHandler(request.param["table_classes"])
    return True
    
@pytest.fixture
def recreateDatabase(dropDatabase, createDatabase)-> bool:
    return dropDatabase and createDatabase

@pytest.mark.parametrize(
    ["createDatabase", "getDatabaseHandler"],
    [{"table_classes": [Contact]}],
    indirect=True
)
def test_contact_sqlite_insertable(recreateDatabase, genContact, getDatabaseHandler):
    c = genContact()
    dbh = getDatabaseHandler
    with dbh.dbEngineInstance as engine:
        engine.add(c)
        engine.commit()
    
    with dbh.dbEngineInstance as engine:
        selectionResult = engine.query(Contact).filter_by(email=c.email).all()
    
    print(selectionResult)
    assert len(selectionResult) == 1, f"output: {selectionResult}, got {len(selectionResult)}"
    assert selectionResult[0][0] == c.email, f"output: {selectionResult[0]}"

