from abc import ABCMeta, abstractmethod
from collections.abc import Iterable
from smtplib import *
from models import User, Contact, Template

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
    def __init__(self, user: User, hostname: str, port: int) -> None:
        self.hostname: str = hostname
        self.port: int = port
        self.user: User = user

    def QueueMails(self, template: Template, contacts: Iterable[Contact]):
        self.contacts = contacts
        self.template = template
        
    def EstablishConnection(self):
        self.server = SMTP_SSL(self.hostname, self.port)
        self.server.ehlo()
        self.server.login()
    
    def Send(self) -> None:
        self.EstablishConnection()
        self.server.send_message(self.template.ToMessage(), self.user.contact.email, self.contacts)
