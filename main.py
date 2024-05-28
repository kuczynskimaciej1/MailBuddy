from MessagingService.senders import *
from MessagingService.readers import *
from UserInfo.LoginService import *
# from sys import platform
from group_controller import GroupController
from models import IModel, Template, Attachment, Contact, Message, Group, User
from Triggers.triggers import ITrigger
from Interface.AppUI import AppUI
from DataSources.dataSources import DatabaseHandler, GapFillSource, IDataSource
from additionalTableSetup import GroupContacts, MessageAttachment, SendAttempt


mocking_enabled = True
mock_name = "Russ"
mock_lastname = "Connelly"
mock_login = "russ.connelly30@ethereal.email"
mock_pwd = "QQcGx1RmfVkaEMjzqZ"

smtp_host = "smtp.ethereal.email"
smtp_port = 587
smtp_security = "tls"



dbname = "localSQLite.sqlite3"
dbURL = f"sqlite:///{dbname}"
tables = [Template, Attachment, Contact, User, ITrigger, Message, Group, MessageAttachment, SendAttempt, GroupContacts]
db: IDataSource = None

    
def pushQueuedInstances():
    if len(IModel.addQueued) > 0:
        for o in IModel.addQueued:
            db.Save(o)
            IModel.addQueued.remove(o)
    if len(IModel.updateQueued) > 0:
        for o in IModel.updateQueued:
            db.Update(o)
            IModel.updateQueued.remove(o)

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
            sender = SMTPSender(mock_user)
        except Exception as e:
            print(e)
        
    
    ui.add_periodic_task(5000, pushQueuedInstances)
    ui.run()
