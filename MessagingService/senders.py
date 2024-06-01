from abc import ABCMeta, abstractmethod
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
        print("PASSWORD: " + u.password)
        print("HOST: " + str(u._smtp_host))
        print("PORT: " + str(u._smtp_port))
        server = SMTP_SSL(u._smtp_host, u._smtp_port)
        server.connect(u._smtp_host, u._smtp_port)
        #server.starttls()
        server.ehlo()
        server.login(u._email, u.password)
        for contact in g.contacts:
            recipient = contact._email
            message = Message()
            server.sendmail(u._email, recipient, message)
        server.quit()
        
# class MockSMTPSender(ISender):
#     def __init__(self) -> None:
        