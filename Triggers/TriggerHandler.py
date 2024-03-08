import MessagingService

class TriggerHandler():
    instance = None
    def __init__(self, sender: ISender, reader: IReader = None) -> None:
        assert TriggerHandler.instance != None
        
        self.sender = sender
        self.reader = reader
        TriggerHandler.instance = self
            