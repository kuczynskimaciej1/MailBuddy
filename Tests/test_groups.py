import pytest
from models import Group, Contact
from SQLite_operations_test import recreateDatabase, getDatabaseHandler, dropDatabase, createDatabase
from additionalTableSetup import GroupContacts
from dataGenerators import genContact

@pytest.mark.parametrize(
    "createDatabase",
    [{"table_classes": [Contact, Group, GroupContacts]}],
    indirect=True
)
def test_group_association_insertable(recreateDatabase, getDatabaseHandler, genContact):
    c: Contact = genContact()
    g: Group = Group(_name="Doesn't matter")
    
    gc = GroupContacts(group_id = g.id, contact_id=c.email)
    
    dbh = getDatabaseHandler
    dbh.Save(gc)
    
    
    selectionResult: list[GroupContacts] = dbh.GetData(GroupContacts)
    
    assert len(selectionResult) == 1
    
    s_gc = selectionResult[0]
    assert s_gc.group_id == g.id 
    assert s_gc.contact_id == c.email
