from MessagingService.senders import *
from MessagingService.readers import *
from UserInfo.LoginService import *
# from sys import platform
import models as m
from Triggers.triggers import ITrigger
from interface import AppUI
from DataSources.dataSources import DatabaseHandler, IDataSource
from additionalTableSetup import MessageAttachment, SendAttempt

dbname = "localSQLite.sqlite3"
dbURL = f"sqlite:///{dbname}"
tables = [m.Template, m.Attachment, m.Contact, ITrigger, m.Message, MessageAttachment, SendAttempt]


def populateInterface(app: AppUI) -> None:
    modelType_func_mapper = {
        m.Template: app.add_template,
        
        }
    
    for (modelType, ui_func) in modelType_func_mapper.items():
        ui_func(modelType.all_instances)
    

if __name__ == "__main__":
    db = DatabaseHandler(dbURL, tables)
    ui = AppUI()
    ui.prepareInterface()
    
    if db.checkIntegrity():
        print("Database intact, proceeding")
    db.LoadSavedState()
    populateInterface(ui)
    
    # TODO win32 powidomienia
    # if 'win32' in platform:
    #     enableWin32Integration()
        
    ui.run()
    
