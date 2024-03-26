from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from abc import ABCMeta, abstractmethod


__all__ = ["Template", "Attachment", "Contact", "User", "Message"]



class IModel(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, *args, **kwargs):
        pass
    
    @abstractmethod
    def getCreateTableString() -> str:
        pass
    
    @abstractmethod
    def getTableName() -> str:
        pass
    
    @abstractmethod
    def getFromDatasource() -> list:
        pass
    
    @abstractmethod
    def postToDatasource():
        pass


class Template(IModel):
    all_instances = []
    tableName = "Templates"
    
    @classmethod
    def getCreateTableString(cls) -> str:
        return f"""CREATE TABLE IF NOT EXISTS {cls.tableName} (
                id INTEGER PRIMARY KEY NOT NULL,
                name VARCHAR(100) NOT NULL,
                content TEXT NOT NULL DEFAULT ''
            );"""
            
    @classmethod
    def getTableName(cls) -> str:
        return cls.tableName
    
    def __init__(self, title, path) -> None:
        self.title = title
        self.content = MIMEText("", 'html')
        self.path = ""
        Template.all_instances.append(self)


class Attachment(IModel):
    all_instances = []
    tableName = "Attachments"
    
    @classmethod
    def getCreateTableString(cls) -> str:
        return f"""CREATE TABLE IF NOT EXISTS {cls.tableName} (
            attachment_id INTEGER PRIMARY KEY NOT NULL,
            name varchar(100) NOT NULL,
            file_path varchar(255),
            file binary DEFAULT ''
        );
        """

    @classmethod
    def getTableName(cls) -> str:
        return cls.tableName
        
    def __init__(self, path, type) -> None:
        self.path = path
        self.type = type
        Attachment.all_instances.append(self)
    
    def prepareAttachment(self):
        att = MIMEApplication(open(self.path, "rb").read(),_subtype=self.type)
        att.add_header('Content-Disposition', "attachment; filename= %s" % self.path.split("\\")[-1])
        return att

    
class Contact(IModel):
    all_instances = []
    tableName = "Contacts"
    
    @classmethod
    def getCreateTableString(cls) -> str:
        return f"""CREATE TABLE IF NOT EXISTS {cls.tableName} (
            email varchar(100) NOT NULL, 
            first_name varchar(50) NOT NULL, 
            last_name varchar(50) NOT NULL,
            PRIMARY KEY(email) 
            );"""

    @classmethod
    def getTableName(cls) -> str:
        return cls.tableName

    def __init__(self, first_name: str, last_name: str, email: str) -> None:
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        Contact.all_instances.append(self)
        
    def __str__(self) -> str:
        return f"Contact {self.first_name} {self.last_name}, {self.email}"
    

    def getFromDatasource() -> list:
        pass
    

    def postToDatasource():
        pass
    
    # def insertContact(self, obj: Contact):
    #     cur = con.cursor()
    #     cur.execute("INSERT INTO Contacts VALUES(?, ?, ?)", (obj.first_name, obj.last_name, obj.email))
    #     self.connection.commit()

    # def getContacts() -> list[Contact]:
    #     con = sqlite3.connect("localSqLite.db")
    #     cur = con.cursor()
    #     result = cur.execute("SELECT first_name, last_name, email from Contacts")
    #     return parseContacts(result.fetchall())

    # def parseContacts(rawData: list) -> list:
    #     result = []
    #     for c in rawData:
    #         result.append(Contact(c[0], c[1], c[2]))
    #     return result

  
class User():
    all_instances = []
    @classmethod
    def getCreateTableString(cls) -> str:
        return None
    
    def __init__(self, first_name, last_name, email, password) -> None:
        self.contact = Contact(first_name, last_name, email)
        self.password = password
        User.all_instances.append(self)

 
class Message(IModel, MIMEMultipart):
    all_instances = []
    tableName = "Messages"
    
    @classmethod
    def getCreateTableString(cls) -> str:
        return f"""CREATE TABLE IF NOT EXISTS {cls.tableName} (
            message_id INTEGER PRIMARY KEY,
            trigger_id INTEGER NOT NULL,
            email varchar(100) NOT NULL,
            template_id INTEGER NOT NULL,
            sent_at TIMESTAMP,
            FOREIGN KEY (trigger_id) REFERENCES Triggers(id),
            FOREIGN KEY (email) REFERENCES Contacts(email),
            FOREIGN KEY (template_id) REFERENCES Templates(id)
        );"""

    @classmethod
    def getTableName(cls) -> str:
        return cls.tableName

    def __init__(self, recipient: Contact, att: list[Attachment] = None) -> None:
        self.recipient = recipient
        self.att = att
        Message.all_instances.append(self)

