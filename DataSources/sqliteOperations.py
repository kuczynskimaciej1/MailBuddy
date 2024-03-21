import sqlite3
from typing import Optional
from models import Template, Attachment, Contact, Message
from Triggers.triggers import ITrigger

class sqlite():
    
    def __init__(self, databaseName: str):
        self.dbName = databaseName
        self.connection = sqlite3.connect(self.dbName)
        
    def checkIntegrity(self) -> bool:
        con = sqlite3.connect(self.dbName)
        cur = con.cursor()
        tableCreators = [Template, Attachment, Contact, ITrigger, Message]
        
        existingTables = cur.execute("SELECT name FROM sqlite_schema WHERE type ='table' AND name NOT LIKE 'sqlite_%';").fetchall()
        
        for classType in tableCreators:
            if classType.getTableName() not in [table[0] for table in existingTables]:
                return False
            
        return True
    
    def createDatabase(self):
        con = sqlite3.connect(self.dbName)
        cur = con.cursor()

        tableCreators = [Template, Attachment, Contact, ITrigger, Message]
        print("TableCreators: " + str(tableCreators))
        for modelClass in tableCreators:
            cmd = modelClass.getCreateTableString()
            if (cmd != None):
                cur.execute(cmd)

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

        for cmd in additionalSetup:
            cur.execute(cmd)
        
        con.commit()

    def FetchAll(self, query: str) -> Optional[str]:
        c = self.connection.cursor()
        result = c.execute(query)
        return result.fetchall()
