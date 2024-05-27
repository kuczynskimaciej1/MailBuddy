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
tables = [Template, Attachment, Contact, ITrigger, Message, Group, MessageAttachment, SendAttempt, GroupContacts]
db: IDataSource = None


def populateInterface(app: AppUI) -> None:
    modelType_func_mapper = {
        Template: app.add_template,
        Group: app.add_group
        }
    
    for (modelType, ui_func) in modelType_func_mapper.items():
        ui_func(modelType.all_instances)
    
def pushQueuedInstances():
    if len(IModel.saveQueued) > 0:
        for o in IModel.saveQueued:
            # match type(o):
            #     case type(Group):
            #         GroupContacts.FromGroup(o)
            #     case _:
            db.Save(o)
            IModel.saveQueued.remove(o)

if __name__ == "__main__":
    db = DatabaseHandler(dbURL, tables)
    GroupController.setDbHandler(db)
    ui = AppUI()
    ui.prepareInterface()
    
    if db.checkIntegrity():
        print("Database intact, proceeding")
    db.LoadSavedState()
    populateInterface(ui)
    
    _contact_fields = GapFillSource()
    
    if (mocking_enabled):
        try:    
            mock_user = User(email=mock_login, 
                            first_name=mock_name, 
                            last_name=mock_lastname, 
                            password=mock_pwd)
            sender = SMTPSender(mock_user)
        except AttributeError as ae:
            print(ae)
    
    ui.add_periodic_task(5000, pushQueuedInstances)
    ui.run()
