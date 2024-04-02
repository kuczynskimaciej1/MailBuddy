from MessagingService.senders import *
from MessagingService.readers import *
from UserInfo.LoginService import *
import models as m
from Triggers.triggers import ITrigger
# from interface import AppUI
from DataSources.dataSources import DatabaseHandler

if __name__ == "__main__":
    dbname = "localSQLite.sqlite3"
    db = DatabaseHandler(connectionString=dbname)
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
    
    db.checkIntegrity(tables, additionalSetup)
    
    #ui = AppUI()
    #ui.prepareInterface()
    #ui.run()

    imap_reader = IMAPReader.getGmailConfig(input("Gmail OAuth2 String"))
    
    
    
    # smtp_sender = SMTPSender()

    loginData = loginPrompt()
    user = m.User(loginData[2], loginData[3], loginData[0], loginData[1])
    imap_reader.login(user.contact.email, user.password)
        
    
    # Get a list of all mailboxes
    status, mailboxes = imap_reader.list()

    # Print the list of mailboxes
    print("Mailboxes:")
    for mailbox in mailboxes:
        print(mailbox.decode())

    # Logout from the server
    imap_reader.logout()
    
