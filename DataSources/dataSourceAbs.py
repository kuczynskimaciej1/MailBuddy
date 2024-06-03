from abc import abstractmethod


class IDataSource():
    current_instance = None
    
    @classmethod
    def __subclasshook__(cls, subclass: type) -> bool:
        return (hasattr(subclass, 'GetData') and 
                callable(subclass.GetData) and
                hasattr(subclass, 'checkIntegrity') and 
                callable(subclass.checkIntegrity) and
                hasattr(subclass, 'LoadSavedState') and 
                callable(subclass.LoadSavedState)
                )
        
    @abstractmethod
    def GetData(self):
        raise RuntimeError
    
    @abstractmethod
    def checkIntegrity(self):
        raise RuntimeError
    
    @abstractmethod
    def LoadSavedState(self):
        """Collect all data saved in data source and instantiate adjacent model objects
        """
        raise RuntimeError