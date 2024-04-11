import pytest
from time import sleep
import os
import sqlite3 # TODO to be changed into SQLAlchemy
from models import Contact
from dataGenerators import genContact
# from DataSources.sqliteOperations import sqlite
from DataSources.dataSources import DatabaseHandler
from sqlalchemy.orm import sessionmaker


localDbName = "localSQLite.sqlite3"
dbURL = f"sqlite:///{localDbName}"

@pytest.fixture
def getDatabaseHandler(request) -> DatabaseHandler:
    return DatabaseHandler(dbURL, [])

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
    dbh = DatabaseHandler(dbURL, (request.param["table_classes"]))
    dbh.instantiateClasses(request.param["table_classes"])
    return True
    
@pytest.fixture
def recreateDatabase(dropDatabase, createDatabase)-> bool:
    return dropDatabase and createDatabase

@pytest.mark.parametrize(
    "createDatabase",
    [{"table_classes": [Contact]}],
    indirect=True
)
def test_contact_sqlite_insertable(recreateDatabase, genContact, getDatabaseHandler):
    c = genContact()
    dbh = getDatabaseHandler
    engine = dbh.dbEngineInstance
    
    Session = sessionmaker(bind=engine)
    with Session() as session:
        session.add(c)
        session.commit()
        session.refresh(c)
    
    
    with Session() as session:
        selectionResult = session.query(Contact).filter_by(email=c.email).all()
    
    print(selectionResult)
    assert len(selectionResult) == 1, f"output: {selectionResult}, got {len(selectionResult)}"
    assert selectionResult[0].email == c.email, f"output: {selectionResult[0]}"

