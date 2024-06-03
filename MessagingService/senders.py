from abc import ABCMeta, abstractmethod
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import *
from models import Group, Template, User, Message

class ISender(metaclass=ABCMeta):
    @abstractmethod
    def Send(self) -> None:
        raise AssertionError
    
    @classmethod
    def __subclasshook__(cls, __subclass: type) -> bool:
        if cls is ISender:
            if any("Send" in B.__dict__ for B in __subclass.__mro__):
                return True
        return NotImplemented

    
class SMTPSender(ISender):

    def Send(self, g: Group, t: Template, u: User) -> None:
        # print("PASSWORD: " + u.password)
        print("HOST: " + str(u._smtp_host))
        print("PORT: " + str(u._smtp_port))
        if not u._smtp_host or not u._smtp_port:
            raise AttributeError("Nie połączyłeś się z serwerem, aby pobrać ustawienia")
        server = SMTP_SSL(u._smtp_host, u._smtp_port)
        server.connect(u._smtp_host, u._smtp_port)
        #server.starttls()
        server.ehlo()
        server.login(u._email, u.password)
        print("logged in successfully")
        emailsSent = 0
        print(f"Sending {t.name} to {len(g.contacts)} contacts")
        for contact in g.contacts:
            print(f"Sending do {contact.email}")
            message = Message(t, contact)
            mimemsg = MIMEMultipart("alternative")
            mimemsg["From"] = u._email
            mimemsg["To"] = contact.email
            mimemsg["Subject"] = "MailBuddy mailing"  # TODO Temat maila w TemplateEditor, aby dało się go parametryzować
            xd = MIMEText(message.getParsedBody(), "html")
            mimemsg.attach(xd)
            server.send_message(mimemsg)
            emailsSent += 1
        server.quit()
        print(f"Sent {emailsSent}")
        
# class MockSMTPSender(ISender):
#     def __init__(self) -> None:
        