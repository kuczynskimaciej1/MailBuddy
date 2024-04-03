from pathlib import Path
import pytest
from faker import Faker
from DataSources.dataSources import DatabaseHandler
from UserInfo.cfgExporter import ConfigExporter, ExportLocation
from models import Contact
from collections.abc import Callable



@pytest.fixture
def generate_contact() -> Callable[[], Contact]:
    def _generator() -> Contact:
        fake = Faker()
        return Contact(fake.first_name(), fake.last_name(), fake.simple_profile()["mail"])
    
    return _generator

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
    # Add assertions as needed


def test_export_contact_to_json(getSampleJsonPath, generate_contact):
    c1 = generate_contact()
    c2 = generate_contact()
    assert c1 != c2
    f = getSampleJsonPath
    print(len(Contact.all_instances))
    exp = ConfigExporter.ToJSON(str(f))
    exp.Export()
    
    with open(f, "r") as r:
        data = r.read()
    assert isinstance(data, str)
    print(data)
    # for contact in [c1, c2]:
        # assert data
    pass
        
