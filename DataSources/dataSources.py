from abc import ABCMeta, abstractmethod
from enum import Enum

class SupportedDbEngines(Enum):
    SQLite=1

class IDataSource(metaclass = ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass: type) -> bool:
        return (hasattr(subclass, 'GetData') and 
                callable(subclass.GetData))
        
    @abstractmethod
    def GetData():
        raise RuntimeError
    
class DatabaseHandler(IDataSource):
    def __init__(self, engine: SupportedDbEngines) -> None:
        pass
    
    def GetData():
        pass
    
class FileInputHandler(IDataSource):
    def __init__(self) -> None:
        pass
    
    def GetData():
        pass