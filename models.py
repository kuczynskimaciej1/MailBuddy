from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from abc import ABCMeta, abstractmethod


__all__ = ["Template", "Attachment", "Contact", "User", "Message"]


class IModelMeta(ABCMeta):
    def __init__(cls, name, bases, namespace):
        super().__init__(name, bases, namespace)
        cls.createTable = ""
        cls.constraints = []
        cls.all_instances = []

class IModel(metaclass=IModelMeta):
    @abstractmethod
    def __init__(self, *args, **kwargs):
        pass


class Template(IModelMeta):
    createTable = """CREATE TABLE IF NOT EXISTS "Templates" (
    "id" INTEGER PRIMARY KEY NOT NULL,
    "name" VARCHAR(100) NOT NULL,
    "content" TEXT NOT NULL DEFAULT ''
);
"""

    constraints = [
        """ALTER TABLE "Templates" ADD CONSTRAINT "Templates_fk0" FOREIGN KEY ("id") REFERENCES "Messages"("template_id");"""
    ]
    
    def __init__(self, title, path) -> None:
        self.title = title
        self.content = MIMEText("", 'html')
        self.path = ""
        Template.all_instances.append(self)


class Attachment(IModel):
    createTable = """CREATE TABLE IF NOT EXISTS "Attachments" (
	"attachment_id" INTEGER PRIMARY KEY NOT NULL,
	"name" varchar(100) NOT NULL,
	"file_path" varchar(255),
	"file" binary DEFAULT ''
);""" 
    def __init__(self, path, type) -> None:
        self.path = path
        self.type = type
        Attachment.all_instances.append(self)
    
    def prepareAttachment(self):
        att = MIMEApplication(open(self.path, "rb").read(),_subtype=self.type)
        att.add_header('Content-Disposition', "attachment; filename= %s" % self.path.split("\\")[-1])
        return att

    
class Contact(IModel):
    createTable = """CREATE TABLE IF NOT EXISTS "Contacts" (
	"contact_id" Integer PRIMARY KEY,
	"first_name" varchar(50) NOT NULL,
	"last_name" varchar(50) NOT NULL,
	"email" varchar(100) NOT NULL
);"""

    def __init__(self, first_name, last_name, email) -> None:
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        Contact.all_instances.append(self)

  
class User(IModel):
    def __init__(self, first_name, last_name, email, password) -> None:
        self.contact = Contact(first_name, last_name, email)
        self.password = password
        User.all_instances.append(self)

 
class Message(IModel, MIMEMultipart):
    createTable = """CREATE TABLE IF NOT EXISTS "Messages" (
	"message_id" integer PRIMARY KEY,
	"trigger_id" integer NOT NULL,
	"contact_id" integer NOT NULL,
	"template_id" integer NOT NULL,
	"sent_at" timestamp
);"""

    constraints = [
        """ALTER TABLE "Messages" ADD CONSTRAINT "Messages_fk1" FOREIGN KEY ("trigger_id") REFERENCES "Triggers"("id");""",
        """ALTER TABLE "Messages" ADD CONSTRAINT "Messages_fk2" FOREIGN KEY ("contact_id") REFERENCES "Contacts"("contact_id");"""
    ]

    def __init__(self, recipient: Contact, att: list[Attachment] = None) -> None:
        self.recipient = recipient
        self.att = att
        Message.all_instances.append(self)

