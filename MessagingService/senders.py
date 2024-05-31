from abc import ABCMeta, abstractmethod
from collections.abc import Iterable
from smtplib import *
import MessagingService.smtp_data

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
    
    @abstractmethod
    def SendEmails(self, g: Group, t: Template, u: User) -> None:
        # TODO: Tworzenie obiektów Message i wysyłka
        raise AssertionError

    
class SMTPSender(ISender):
    
    def SendEmails(self, g: Group, t: Template, u: User) -> None:
        # TODO: Tworzenie obiektów Message i wysyłka
        raise NotImplementedError
    
    def Send(self, host, port, email, password, message, recipient) -> None:
        smtp_host = host
        smtp_port = port
        print("PASSWORD: " + password)
        print("RECIPIENT: " + recipient)
        print("HOST: " + str(smtp_host))
        print("PORT: " + str(smtp_port))
        server = SMTP(smtp_host, smtp_port)
        server.connect(smtp_host, smtp_port)
        server.starttls()
        server.ehlo()
        server.login(email, password)
        server.sendmail(email, recipient, message)
        server.quit()
        
# class MockSMTPSender(ISender):
#     def __init__(self) -> None:
        