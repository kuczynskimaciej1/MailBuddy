from abc import ABCMeta, abstractmethod
from smtplib import *

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
    def Send() -> None:
        smtp_host = "" #hostname
        smtp_port = 123
        server = SMTP_SSL(smtp_host, smtp_port)
        server.connect(smtp_host, smtp_port)
        server.ehlo()
        server.login()
        pass