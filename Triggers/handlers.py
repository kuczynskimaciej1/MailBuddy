from MessagingService.readers import IReader, IMAPReader
from MessagingService.senders import ISender, SMTPSender

class TriggerHandler():
    instance = None
    def __init__(self, sender: ISender=None, reader: IReader = None) -> None:
        assert TriggerHandler.instance == None
        
        self.sender = sender
        self.reader = reader
        TriggerHandler.instance = self
