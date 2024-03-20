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
    def GetData(self):
        raise RuntimeError
    
class DatabaseHandler(IDataSource):
    def __init__(self, engine: SupportedDbEngines) -> None:
        pass
    
    def GetData(self):
        pass
    
class XLSXHandler(IDataSource):
    def __init__(self, path: str) -> None:
        self.file_path = path
    
    def GetData(self) -> pd.DataFrame:
        """otwiera plik XLS"""
        try:
            data = pd.read_excel(self.file_path)
            return data
        except Exception as e:
            print("Błąd podczas wczytywania pliku XLSX:", e)
            return None


class CSVXHandler(IDataSource):
    def __init__(self, path: str) -> None:
        self.file_path = path
        
    
    def GetData(self) -> pd.DataFrame:
        """otwiera plik csv"""
        try:
            data = pd.read_csv(self.file_path)
            return data
        except Exception as e:
            print("Błąd podczas wczytywania pliku CSV:", e)
            return None