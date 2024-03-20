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


class Template(IModel):
    all_instances = []
    def getCreateTableString() -> str:
        return """CREATE TABLE IF NOT EXISTS Templates (
                id INTEGER PRIMARY KEY NOT NULL,
                name VARCHAR(100) NOT NULL,
                content TEXT NOT NULL DEFAULT ''
            );"""
    
    def __init__(self, title, path) -> None:
        self.title = title
        self.content = MIMEText("", 'html')
        self.path = ""
        Template.all_instances.append(self)


class Attachment(IModel):
    all_instances = []
    def getCreateTableString() -> str:
        return """CREATE TABLE IF NOT EXISTS Attachments (
	attachment_id INTEGER PRIMARY KEY NOT NULL,
	name varchar(100) NOT NULL,
	file_path varchar(255),
	file binary DEFAULT ''
);
""" 
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
    def getCreateTableString() -> str:
        return """CREATE TABLE IF NOT EXISTS Contacts (
            email varchar(100) NOT NULL, 
            first_name varchar(50) NOT NULL, 
            last_name varchar(50) NOT NULL,
            PRIMARY KEY(email) 
            );"""

    def __init__(self, first_name, last_name, email) -> None:
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        Contact.all_instances.append(self)
        
    def __str__(self) -> str:
        return f"Contact {self.first_name} {self.last_name}, {self.email}"

  
class User(IModel):
    def getCreateTableString() -> str:
        return None
    
    def __init__(self, first_name, last_name, email, password) -> None:
        self.contact = Contact(first_name, last_name, email)
        self.password = password
        User.all_instances.append(self)

 
class Message(IModel, MIMEMultipart):
    all_instances = []
    def getCreateTableString() -> str:
        return """CREATE TABLE IF NOT EXISTS Messages (
    message_id INTEGER PRIMARY KEY,
    trigger_id INTEGER NOT NULL,
    email varchar(100) NOT NULL,
    template_id INTEGER NOT NULL,
    sent_at TIMESTAMP,
    FOREIGN KEY (trigger_id) REFERENCES Triggers(id),
    FOREIGN KEY (email) REFERENCES Contacts(email),
    FOREIGN KEY (template_id) REFERENCES Templates(id)
);"""

    def __init__(self, recipient: Contact, att: list[Attachment] = None) -> None:
        self.recipient = recipient
        self.att = att
        Message.all_instances.append(self)

