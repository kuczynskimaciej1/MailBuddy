from abc import ABCMeta, abstractmethod

class IReader(metaclass=ABCMeta):
    @abstractmethod
    def ReadAll() -> None:
        raise AssertionError
    
    @classmethod
    def __subclasshook__(cls, __subclass: type) -> bool:
        if cls is IReader:
            if any("ReadAll" in B.__dict__ for B in __subclass.__mro__):
                return True
        return NotImplemented
   


    
