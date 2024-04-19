from MessagingService.senders import *
from MessagingService.readers import *
from UserInfo.LoginService import *
# from sys import platform
from group_controller import GroupController
from models import IModel, Template, Attachment, Contact, Message, Group
from Triggers.triggers import ITrigger
from interface import AppUI
from DataSources.dataSources import DatabaseHandler, IDataSource
from additionalTableSetup import GroupContacts, MessageAttachment, SendAttempt

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
    gc = GroupController(db)
    ui = AppUI()
    ui.prepareInterface()
    
    if db.checkIntegrity():
        print("Database intact, proceeding")
    db.LoadSavedState()
    populateInterface(ui)
    
    # TODO win32 powidomienia
    # if 'win32' in platform:
    #     enableWin32Integration()

    ui.add_periodic_task(5000, pushQueuedInstances)
    ui.run()
