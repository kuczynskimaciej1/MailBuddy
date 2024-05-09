from additionalTableSetup import GroupContacts
from models import Group, Contact
from DataSources.dataSources import DatabaseHandler

class GroupController:
    dbh: DatabaseHandler = None
    @classmethod
    def setDbHandler(cls, handler: DatabaseHandler) -> None:
        cls.dbh = handler
    
    @classmethod
    def add_contact(cls, g: Group, c: Contact) -> None:
        if g._add_contact(c):
            gc = GroupContacts(group_id=g.id, contact_id=c.email)
            cls.dbh.Save(gc)
        
    @classmethod
    def delete_connection(cls, g: Group, c: Contact) -> None:
        connections :list[GroupContacts] = cls.dbh.GetData(GroupContacts, group_id=g.id, contact_id=c.email)
        for con in connections:
            cls.dbh.DeleteEntry(con)
            del con
    
    @classmethod
    def get_contacts(cls, g: Group) -> list[Contact]:
        mapping = cls.dbh.GetData(GroupContacts, group_id=g.id)
        # TODO: Wydajność? Wywołania tego na potencjalnie ogromnej tabeli to spory koszt, na pewno można to jakoś kiedyś ładnie zoptymalizować
        result = []
        for entry in mapping:
            result.append(*cls.dbh.GetData(Contact, email=entry.contact_id))
        return result
