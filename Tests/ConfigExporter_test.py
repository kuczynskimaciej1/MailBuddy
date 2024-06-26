from collections.abc import Callable
import pytest
import json
from pathlib import Path
from UserInfo.cfgExporter import ConfigExporter, ExportLocation
from models import Contact
# from models import __all__ as modelClassNames

@pytest.fixture
def getSampleJsonPath(tmp_path: Path) -> Path:
    return tmp_path / "test.json"


def test_json_exporter_factory(getSampleJsonPath: Path):
    p = getSampleJsonPath
    exporter = ConfigExporter.ToJSON(p)
    assert isinstance(exporter, ConfigExporter)
    assert exporter.export == ExportLocation.JSON
    assert exporter.location == p


def test_export_to_json(getSampleJsonPath: Path):
    filename = getSampleJsonPath
    exporter = ConfigExporter.ToJSON(str(filename))
    exporter.Export()
    filename = Path(exporter.location)
    assert filename.exists()
    
    with open(filename, "r") as r:
        assert isinstance(r.read(), str)


def test_export_contact_to_json(getSampleJsonPath: Path, genContact: Callable[[], Contact]):
    c1 = genContact()
    c2 = genContact()
    assert c1 != c2
    f = getSampleJsonPath
    print(len(Contact.all_instances))
    
    exp = ConfigExporter.ToJSON(str(f))
    exp.Export()
    
    with open(f, "r") as r:
        unparsed = r.read()
    contacts_data = json.loads(unparsed)["Contacts"]
    unparsedContacts = [Contact(**contact) for contact in contacts_data]
    assert isinstance(unparsedContacts, list) and len(unparsedContacts) == len([c1, c2])
    for exported, org in zip(unparsedContacts, [c1, c2]):
        assert exported == org


# def test_to_database(db_handler):
#     exporter = ConfigExporter.ToDatabase(db_handler)
#     assert isinstance(exporter, ConfigExporter)
#     assert exporter.export == ExportLocation.Database
#     assert exporter.location == db_handler