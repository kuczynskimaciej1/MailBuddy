from abc import ABCMeta, abstractmethod
from typing import Iterable
from enum import Enum
from pandas import read_csv, read_excel, DataFrame
from .sqliteOperations import sqlite
import re

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
    def __init__(self, connectionString: str,  engine: SupportedDbEngines = SupportedDbEngines.SQLite) -> None:
        """
        Initializes handler, allowing query execution on provided server
        """
        match engine:
            case SupportedDbEngines.SQLite:
                self.dbEngineInstance = sqlite(connectionString)
            case _:
                raise NotImplementedError
        self.query = ""
        self.parameters = []


    def checkIntegrity(self) -> None:
        if self.dbEngineInstance.checkIntegrity() == False:
            print("Remaking db")
            self.dbEngineInstance.createDatabase()
            return
        print("Database intact, proceeding")
        
    
    
    def SetQuery(self, query: str, parameters: Iterable[object] = []) -> None:
        query = query.strip()
        
        firstSemicolonIndex = query.index(";")
        if firstSemicolonIndex != len(query) - 1:
            raise AttributeError(f"This method executes only single statement queries, found ; on {firstSemicolonIndex}")
                
        parameterSearchPattern = r'\(\?(?:,\s*\?\s*)*\)'
        match = re.match(parameterSearchPattern, query)
        if match:
            question_marks = match.group(1).count('?')
            if len(parameters) != question_marks:
                raise AttributeError(f"You provided {len(parameters)}, expected {question_marks}")
            else:
                self.parameters = parameters
        
        self.query = query

    # is it even legal in our case?
    # def SetMultiStatementQuery(self, query: str, parameters: Iterable = []) -> None:
    #     query = query.strip()
    #     self.query = query
        
    #     if len(parameters) != 0:
    #         self.parameters = parameters


    def GetData(self) -> str:
        # TODO pewnie będzie trzeba dopisać później na mniejsze fetche
        assert self.query != ""
        
        result = self.dbEngineInstance.FetchAll(self.query)
        
        self.query = ""
        self.parameters = []
        
        return result
        
    
    def GetData(self):
        pass


class XLSXHandler(IDataSource):
    def __init__(self, path: str) -> None:
        self.file_path = path
    
    def GetData(self) -> DataFrame:
        """otwiera plik XLS"""
        try:
            data = read_excel(self.file_path)
            return data
        except Exception as e:
            print("Błąd podczas wczytywania pliku XLSX:", e)
            return None


class CSVXHandler(IDataSource):
    def __init__(self, path: str) -> None:
        self.file_path = path
        
    
    def GetData(self) -> DataFrame:
        """otwiera plik csv"""
        try:
            data = read_csv(self.file_path)
            return data
        except Exception as e:
            print("Błąd podczas wczytywania pliku CSV:", e)
            return None