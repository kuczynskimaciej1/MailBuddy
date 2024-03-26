from abc import abstractmethod
from models import IModel

class ITrigger(IModel):
    tableName = "Triggers"
    
    
    @classmethod
    def getCreateTableString(cls) -> str:
        return f"""CREATE TABLE IF NOT EXISTS {cls.tableName} (
            "id" int NOT NULL,
            "name" varchar(100) NOT NULL,
            "type" int NOT NULL,
            "script" text NOT NULL DEFAULT '',
            PRIMARY KEY ("id")
            );"""
            
    @classmethod
    def getTableName(cls) -> str:
        return cls.tableName
    
    @abstractmethod
    def CheckConditions():
        raise AssertionError
    
    @abstractmethod
    def Run():
        raise AssertionError
    
    @classmethod
    def __subclasshook__(cls, subclass: type) -> bool:
        return (hasattr(subclass, 'CheckConditions') and 
                callable(subclass.CheckConditions) and 
                hasattr(subclass, 'Run') and 
                callable(subclass.Run))

class Win32Trigger(ITrigger):
    def __init__(self) -> None:
        pass
