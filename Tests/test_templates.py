from pathlib import Path
import pytest
import os
import sqlite3
from SQLite_operations_test import *
from models import Template
from DataSources.sqliteOperations import sqlite

# localDbName = "test_localSQLite.sqlite3"
insertCommand = "INSERT INTO Templates (name, content) VALUES (?, ?)"
selectCommand = "SELECT name, content FROM Templates WHERE name = ?"

testSamplesPath = os.path.join(os.getcwd(), "Tests/Samples")

@pytest.fixture(scope="module", params=[
    (key, os.path.join(testSamplesPath, value)) 
    for key, value in {
        "Test Template 1": "test_template_1.html",
        "tt": "test_template_2.html",
        "MyThirdRealTemplate": "test_template_3.html",
        "T4": "test_template_4.html",
        "Template 5": "test_template_5.html"
    }.items()])
def getTemplate(request) -> Template:
    result = Template(request.param[0], request.param[1])
    result.getFromDatasource()
    return result

def test_samples_exist(getTemplate):
    t = getTemplate
    assert Path(t.path).exists(), f"File {t.path} does not exist!"
    
    with open(t.path) as r:
        assert r.read() != ""

@pytest.mark.parametrize(
    "createDatabase",
    [{"table_classes": [Template]}],
    indirect=True
)
def test_template_sqlite_insertable(recreateDatabase, sqliteConnection, getTemplate):
    t = getTemplate
    parameters = (t.title, str(t.content))

    sqliteConnection.cursor().execute(insertCommand, parameters)
    sqliteConnection.commit()

    cursor = sqliteConnection.cursor().execute(selectCommand, (t.title, ))
    result = cursor.fetchone()

    assert result is not None
    assert result[0] == t.title
    assert result[1] == str(t.content)