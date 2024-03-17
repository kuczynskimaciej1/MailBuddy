import sqlite3
from models import Template, Attachment, Contact, Message
from Triggers.triggers import ITrigger


def createDatabase(databaseName: str):
    con = sqlite3.connect(databaseName)
    cur = con.cursor()

    tableCreators = [Template, Attachment, Contact, Message, ITrigger]  # to trzeba przetestować
    print("TableCreators: " + str(tableCreators))
    for modelClass in tableCreators:
        # print(modelClass)
        # print(getattr(modelClass, "createTable"))
        cmd = getattr(modelClass, "createTable")
        # print("cmd: " + str(cmd))
        if (cmd != ""):
            cur.execute(cmd)
    print("successfully created tables")


    for modelClass in tableCreators:
        cmds = modelClass.constraints
        for c in cmds:
            if c != "":
                cur.execute(c)
    print("successfully created constraints")

    additionalSetup = [ 
    """CREATE TABLE IF NOT EXISTS "Message_Attachments" (
        "attachment_id" int NOT NULL DEFAULT '',
        "message_id" int NOT NULL DEFAULT '',
        PRIMARY KEY ("attachment_id", "message_id"),
        CONSTRAINT "Message_Attachments_fk0" FOREIGN KEY ("attachment_id") REFERENCES "Attachments"("attachment_id"),
        CONSTRAINT "Message_Attachments_fk1" FOREIGN KEY ("message_id") REFERENCES "Messages"("message_id")
    );""",

    """CREATE TABLE IF NOT EXISTS "Send_attempts" (
        "message_id" int NOT NULL DEFAULT '',
        "attempt" int NOT NULL,
        "timestamp" timestamp NOT NULL,
        "error_message" varchar(200) DEFAULT '',
        PRIMARY KEY ("message_id", "attempt"),
        CONSTRAINT "Send_attempts_fk0" FOREIGN KEY ("message_id") REFERENCES "Messages"("message_id")
    );"""
    ]

    for cmd in additionalSetup:
        cur.execute(cmd)
        
    print("successfully executed additional setup steps")
    con.commit()

def insertContact(obj: Contact):
    con = sqlite3.connect("localSqLite.db")
    cur = con.cursor()
    cur.execute("INSERT INTO Contacts VALUES(?, ?, ?)", obj.first_name, obj.last_name, obj.email)
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
