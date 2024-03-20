import sqlite3
from models import Template, Attachment, Contact, Message
from Triggers.triggers import ITrigger


def createDatabase(databaseName: str):
    con = sqlite3.connect(databaseName)
    cur = con.cursor()

    tableCreators = [Template, Attachment, Contact, ITrigger, Message]
    print("TableCreators: " + str(tableCreators))
    for modelClass in tableCreators:
        cmd = ""
        ct = modelClass.createTable
        if ct:
            print(ct)
            cmd = ct
        else:
            print("No createTable attribute defined for", modelClass)
        
        if (cmd != ""):
            cur.execute(cmd)
    print("CREATE TABLEs executed (hopefully)")


    for modelClass in tableCreators:
        cmds = modelClass.constraints
        for c in cmds:
            if c != "":
                try:
                    cur.execute(c)
                except sqlite3.OperationalError as e:
                    raise AttributeError(f"Error while executing {c}, Error: {e}")
    print("constraints executed (hopefully)")

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
        
    print("successfully executed additional setup steps")
    con.commit()

def insertContact(obj: Contact):
    con = sqlite3.connect("localSqLite.db")
    cur = con.cursor()
    cur.execute("INSERT INTO Contacts VALUES(?, ?, ?)", (obj.first_name, obj.last_name, obj.email))
    con.commit()

def getContacts() -> list[Contact]:
    con = sqlite3.connect("localSqLite.db")
    cur = con.cursor()
    result = cur.execute("SELECT * from Contacts")
    return parseContacts(result.fetchall())

def parseContacts(result: list) -> list:
    for c in result:
        print(c)
        print(c)

def insertData(table, rawData):
    cur = sqlite3.connect("localSqLite.db").cursor()
    

def sqlInjectionCleaner(text: str):
    return text.replace(";")
