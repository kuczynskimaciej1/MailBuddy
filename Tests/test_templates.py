from pathlib import Path
import pytest
import os
import sqlite3
from SQLite_operations_test import *
from models import Template

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
    with open(request.param[1], "rb") as rb:
        result = Template(request.param[0], rb.read())
    return result


@pytest.mark.parametrize(
    "createDatabase",
    [{"table_classes": [Template]}],
    indirect=True
)
def test_template_sqlite_insertable(recreateDatabase, getDatabaseHandler, getTemplate):
    t = getTemplate
    dbh = getDatabaseHandler
    engine = dbh.dbEngineInstance
    
    Session = sessionmaker(bind=engine)
    with Session() as session:
        session.add(t)
        session.commit()
        session.refresh(t)

    with Session() as session:
        selectionResult: list[Template] = session.query(Template).filter_by(name=t.name).all()
    
    assert selectionResult is not None
    assert len(selectionResult) == 1
    
    retrievedTemplate: Template = selectionResult[0]
    assert retrievedTemplate.name == t.name
    assert retrievedTemplate.content == t.content