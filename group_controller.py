from additionalTableSetup import GroupContacts
from models import Group, Contact
from DataSources.dataSources import DatabaseHandler

class GroupController:
    def __init__(self, dbh: DatabaseHandler) -> None:
        self.dbh: DatabaseHandler = dbh
    
    def add_contact(self, g: Group, c: Contact) -> None:
        if g._add_contact(c):
            gc = GroupContacts(group_id=g.id, contact_id=c.email)
            self.dbh.Save(gc)
            
    # TODO delete contact binding?
        
    def get_contacts(self, g: Group) -> list[Contact]:
        return self.dbh.GetData(GroupContacts, group_id=g.id)