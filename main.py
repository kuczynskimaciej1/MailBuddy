from MessagingService.senders import *
from MessagingService.readers import *
from UserInfo.LoginService import *
from models import *
# from interface import AppUI
from DataSources.dataSources import DatabaseHandler

if __name__ == "__main__":
    dbname = "localSQLite.sqlite3"
    db = DatabaseHandler(connectionString=dbname)
    db.checkIntegrity()
    
    
    #ui = AppUI()
    #ui.prepareInterface()
    #ui.run()

    imap_reader = IMAPReader()
    smtp_sender = SMTPSender()

    loginData = loginPrompt()
    user = User(loginData[2], loginData[3], loginData[0], loginData[1])
    
    
