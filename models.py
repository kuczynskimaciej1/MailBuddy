from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

__all__ = ["Template", "Attachment", "Contact", "User", "Message"]

class Template():
    allInstances = []
    def __init__(self, title, path) -> None:
        self.title = title
        self.content = MIMEText("", 'html')
        self.path = ""
        Template.allInstances.append(self)
    
class Attachment():
    allInstances = []
    
    def __init__(self, path, type) -> None:
        self.path = path
        self.type = type
        Attachment.allInstances.append(self)
    
    def prepareAttachment(self):
        att = MIMEApplication(open(self.path, "rb").read(),_subtype=self.type)
        att.add_header('Content-Disposition', "attachment; filename= %s" % self.path.split("\\")[-1])
        return att

    
class Contact():
    allInstances = []
    def __init__(self, first_name, last_name, email) -> None:
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        Contact.allInstances.append(self)
    
class User():
    allInstances = []
    def __init__(self, first_name, last_name, email, password) -> None:
        self.contact = Contact(first_name, last_name, email)
        self.password = password
        User.allInstances.append(self)
    
class Message(MIMEMultipart):
    allInstances = []
    def __init__(self, recipient: Contact, att: list[Attachment] = None) -> None:
        self.recipient = recipient
        self.att = att
        Message.allInstances.append(self)

