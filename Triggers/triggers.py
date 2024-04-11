from abc import abstractmethod, ABCMeta
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

class ITrigger(declarative_base()):
    __tablename__ = "Triggers"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    type = Column(Integer, nullable=False)
    script = Column(String, nullable=False)
    
    @abstractmethod
    def CheckConditions():
        raise AssertionError
    
    @abstractmethod
    def Run():
        raise AssertionError
    
    @classmethod
    def __subclasshook__(cls, subclass) -> bool:
        return (hasattr(subclass, 'CheckConditions') and 
                callable(subclass.CheckConditions) and 
                hasattr(subclass, 'Run') and 
                callable(subclass.Run))

class Win32Trigger(ITrigger, ):
    def __init__(self) -> None:
        pass
