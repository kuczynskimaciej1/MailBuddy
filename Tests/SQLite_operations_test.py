import pytest
import os
from models import Contact
from dataGenerators import genContact
from DataSources.dataSources import DatabaseHandler


localDbName = "localSQLite.sqlite3"
dbURL = f"sqlite:///{localDbName}"

@pytest.fixture
def getDatabaseHandler(request) -> DatabaseHandler:
    return DatabaseHandler(dbURL, [])

@pytest.fixture
def dropDatabase() -> bool:
    if os.path.exists(localDbName):
        try:
            os.remove(path=localDbName)
            return True
        except Exception as e:
            print(e)
            raise e
    return False

@pytest.fixture
def createDatabase(request) -> bool:
    try:
        dbh = DatabaseHandler(dbURL, request.param["table_classes"])
        dbh.instantiateClasses(request.param["table_classes"])
        return True
    except Exception as e:
        print(f"Error creating database: {e}")
        return False
    
@pytest.fixture
def recreateDatabase(dropDatabase, createDatabase)-> bool:
    if dropDatabase and createDatabase:
        return True
    raise OSError("Recreating db failed")

@pytest.mark.parametrize(
    "createDatabase",
    [{"table_classes": [Contact]}],
    indirect=True
)
def test_contact_sqlite_insertable(recreateDatabase, genContact, getDatabaseHandler):
    c = genContact()
    dbh = getDatabaseHandler
    dbh.Save(c)
    
    selectionResult = dbh.GetData(Contact, email=c.email)
    
    print(selectionResult)
    assert len(selectionResult) == 1, f"output: {selectionResult}, got {len(selectionResult)}"
    assert selectionResult[0].email == c.email, f"output: {selectionResult[0]}"

