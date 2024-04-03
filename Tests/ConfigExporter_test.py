import pytest
import json
from pathlib import Path
from DataSources.dataSources import DatabaseHandler
from UserInfo.cfgExporter import ConfigExporter, ExportLocation
from models import Contact
from dataGenerators import genContact
# from models import __all__ as modelClassNames

@pytest.fixture
def getSampleJsonPath(tmp_path) -> Path:
    return tmp_path / "test.json"

def test_to_database(db_handler):
    exporter = ConfigExporter.ToDatabase(db_handler)
    assert isinstance(exporter, ConfigExporter)
    assert exporter.export == ExportLocation.Database
    assert exporter.location == db_handler

def test_json_exporter_factory(getSampleJsonPath):
    p = getSampleJsonPath
    exporter = ConfigExporter.ToJSON(p)
    assert isinstance(exporter, ConfigExporter)
    assert exporter.export == ExportLocation.JSON
    assert exporter.location == p

def test_export_to_database():
    pass
    # exporter = ConfigExporter(ExportLocation.Database, db_handler)
    # exporter.Export()

def test_export_to_json(getSampleJsonPath):
    filename = getSampleJsonPath
    exporter = ConfigExporter.ToJSON(str(filename))
    exporter.Export()
    assert filename.exists()
    
    with open(filename, "r") as r:
        assert isinstance(r.read(), str)


def test_export_contact_to_json(getSampleJsonPath, genContact):
    c1 = genContact()
    c2 = genContact()
    assert c1 != c2
    f = getSampleJsonPath
    print(len(Contact.all_instances))
    
    exp = ConfigExporter.ToJSON(str(f))
    exp.Export()
    
    with open(f, "r") as r:
        data = r.read()
    unparsedContacts = [json.loads(c) for c in data]
    assert isinstance(unparsedContacts, list) and len(unparsedContacts) == len([c1, c2])
    # for exported, org in zip(, [c1, c2]):
    #     exported.
        
    
    # for contact in [c1, c2]:
        # assert data
    pass
        
