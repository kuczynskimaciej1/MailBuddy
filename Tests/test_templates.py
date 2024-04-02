import pytest
import os
import sqlite3
from models import Template
from DataSources.sqliteOperations import sqlite

localDbName = "test_localSQLite.sqlite3"
insertCommand = "INSERT INTO Templates (name, content) VALUES (?, ?)"
selectCommand = "SELECT name, content FROM Templates WHERE name = ?"

@pytest.fixture
def template1():
    return Template("Test Template 1", "test_template_1.html")

@pytest.fixture
def sqlite_connection():
    conn = sqlite3.connect(localDbName)
    yield conn
    conn.close()

@pytest.fixture
def drop_database():
    if os.path.exists(localDbName):
        os.remove(path=localDbName)
        return True
    return False
        
@pytest.fixture
def create_database():
    test_handler = sqlite(localDbName)
    test_handler.createDatabase([Template])
    return True
    
@pytest.fixture
def recreate_database(drop_database, create_database):
    return drop_database and create_database

def test_template_sqlite_insertable(recreate_database, template1, sqlite_connection):
    t = template1
    parameters = (t.title, t.content.as_string())
    
    sqlite_connection.cursor().execute(insertCommand, parameters)
    sqlite_connection.commit()
    
    cursor = sqlite_connection.cursor().execute(selectCommand, (t.title, ))
    result = cursor.fetchone()
    
    assert result is not None
    assert result[0] == t.title
    assert result[1] == t.content.as_string()