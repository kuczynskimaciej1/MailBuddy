from abc import ABCMeta, abstractmethod

class ITrigger(metaclass=ABCMeta):
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
