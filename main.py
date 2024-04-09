from MessagingService.senders import *
from MessagingService.readers import *
from UserInfo.LoginService import *
# from sys import platform
import models as m
from Triggers.triggers import ITrigger
from interface import AppUI
from DataSources.dataSources import DatabaseHandler, IDataSource
import databaseSetup

dbname = "localSQLite.sqlite3"
tables = [m.Template, m.Attachment, m.Contact, ITrigger, m.Message]
additionalSetup = [ 
        """CREATE TABLE IF NOT EXISTS Message_Attachments (
            attachment_id INTEGER NOT NULL,
            message_id INTEGER NOT NULL,
            PRIMARY KEY (attachment_id, message_id),
            FOREIGN KEY (attachment_id) REFERENCES Attachments(attachment_id),
            FOREIGN KEY (message_id) REFERENCES Messages(message_id)
        );""",
        
        """CREATE TABLE IF NOT EXISTS Send_attempts (
            message_id INTEGER NOT NULL,
            attempt INTEGER NOT NULL,
            timestamp TIMESTAMP NOT NULL,
            error_message VARCHAR(200) DEFAULT '',
            PRIMARY KEY (message_id, attempt),
            FOREIGN KEY (message_id) REFERENCES Messages(message_id)
        );"""
    ]


additionalSetup.append(databaseSetup.views)

def populateInterface(app: AppUI) -> None:
    modelType_func_mapper = {m.Template: AppUI.add_template}  # TODO dodać mappery
    for (modelType, ui_func) in modelType_func_mapper.items():
        app.ui_func(modelType.all_instances)
    

if __name__ == "__main__":
    db = DatabaseHandler(dbname, tables)
    ui = AppUI()
    ui.prepareInterface()
    
    if db.checkIntegrity(additionalSetup):
        print("Database intact, proceeding")
        # db.LoadSavedState()
        # populateInterface(ui, tables)
    
    # TODO win32 powidomienia
    # if 'win32' in platform:
    #     enableWin32Integration()
        
    ui.run()
    
