import pytest
import warnings
from models import *
from DataSources.dataSources import DatabaseHandler
from UserInfo.cfgExporter import ConfigExporter, ExportLocation

@pytest.fixture

def test_to_database(db_handler):
    exporter = ConfigExporter.ToDatabase(db_handler)
    assert isinstance(exporter, ConfigExporter)
    assert exporter.export == ExportLocation.Database
    assert exporter.location == db_handler

def test_json_exporter_factory():
    filename = "test.json"
    exporter = ConfigExporter.ToJSON(filename)
    assert isinstance(exporter, ConfigExporter)
    assert exporter.export == ExportLocation.JSON
    assert exporter.location == filename

def test_export_to_database():
    raise NotImplementedError
    # exporter = ConfigExporter(ExportLocation.Database, db_handler)
    # exporter.Export()

def test_export_to_json(tmp_path):
    filename = tmp_path / "test.json"
    exporter = ConfigExporter.ToJSON(str(filename))
    exporter.Export()
    assert filename.exists()
    
    with open(filename, "r") as r:
        assert isinstance(r.read(), str)
    # Add assertions as needed
