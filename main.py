from MessagingService.senders import *
from MessagingService.readers import *
from UserInfo.LoginService import *
# from sys import platform
from group_controller import GroupController
from models import DataImport, IModel, Template, Attachment, Contact, Message, Group, User
from Triggers.triggers import ITrigger
from Interface.AppUI import AppUI
from DataSources.dataSources import DatabaseHandler, GapFillSource, IDataSource
from additionalTableSetup import GroupContacts, MessageAttachment, SendAttempt
from MessagingService.smtp_data import smtp_security, smtp_host, smtp_port

mocking_enabled = False
mock_name = "Russ"
mock_lastname = "Connelly"
mock_login = "russ.connelly30@ethereal.email"
mock_pwd = "QQcGx1RmfVkaEMjzqZ"



dbname = "localSQLite.sqlite3"
dbURL = f"sqlite:///{dbname}"
tables = [Template, DataImport, Attachment, Contact, User, ITrigger, Message, Group, MessageAttachment, SendAttempt, GroupContacts]
global db
db: IDataSource = None

    
if __name__ == "__main__":
    db = DatabaseHandler(dbURL, tables)
    GroupController.setDbHandler(db)
    
    if db.checkIntegrity():
        print("Database intact, proceeding")
    db.LoadSavedState()
    
    ui = AppUI()
    ui.prepareInterface()
    
    
    
    _contact_fields = GapFillSource()
    
    if (mocking_enabled):
        try:    
            mock_user = User(_email=mock_login, 
                            _first_name=mock_name, 
                            _last_name=mock_lastname, 
                            _password=mock_pwd)
            sender = SMTPSender()
        except Exception as e:
            print(e)

    sender = SMTPSender()
    ui.setSender(sender)

    # user = 
    # User(_email="russ.connelly30@ethereal.email", _password="QQcGx1RmfVkaEMjzqZ", _first_name="Russ", _last_name="Connelly", _selected=True)
    # ui.setUser(user)
    
    # ui.add_periodic_task(5000, pushQueuedInstances)
    ui.run()
