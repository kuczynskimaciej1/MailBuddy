from MessagingService.senders import *
from MessagingService.readers import *
from UserInfo.LoginService import *
# from sys import platform
import models as m
from Triggers.triggers import ITrigger
from interface import AppUI
from DataSources.dataSources import DatabaseHandler, IDataSource
from sqlalchemy import Table, Column, PrimaryKeyConstraint, ForeignKeyConstraint, TIMESTAMP, VARCHAR, Integer

dbname = "localSQLite.sqlite3"
dbURL = f"sqlite:///{dbname}"
tables = [m.Template, m.Attachment, m.Contact, ITrigger, m.Message]
# additionalSetup = [
#     Table(
#     'Message_Attachments',
#     Column('attachment_id', Integer, nullable=False),
#     Column('message_id', Integer, nullable=False),
#     PrimaryKeyConstraint('attachment_id', 'message_id'),
#     ForeignKeyConstraint(['attachment_id'], ['Attachments.attachment_id']),
#     ForeignKeyConstraint(['message_id'], ['Messages.message_id'])
# ),
#     Table('Send_attempts',
#         Column('message_id', Integer, nullable=False),
#         Column('attempt', Integer, nullable=False),
#         Column('timestamp', TIMESTAMP, nullable=False),
#         Column('error_message', VARCHAR(200), server_default=''),
#         PrimaryKeyConstraint('message_id', 'attempt'),
#         ForeignKeyConstraint(['message_id'], ['Messages.message_id'])
#     )
# ]

def populateInterface(app: AppUI) -> None:
    modelType_func_mapper = {m.Template: AppUI.add_template}  # TODO dodać mappery
    for (modelType, ui_func) in modelType_func_mapper.items():
        app.ui_func(modelType.all_instances)
    

if __name__ == "__main__":
    db = DatabaseHandler(dbURL, tables)
    ui = AppUI()
    ui.prepareInterface()
    
    if db.checkIntegrity(): # additionalSetup
        print("Database intact, proceeding")
    
    # db.LoadSavedState()
    # populateInterface(ui, tables)
    
    # TODO win32 powidomienia
    # if 'win32' in platform:
    #     enableWin32Integration()
        
    ui.run()
    
