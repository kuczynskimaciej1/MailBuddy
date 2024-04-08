from abc import ABCMeta, abstractmethod
from collections.abc import Iterable
from enum import Enum
from pandas import read_csv, read_excel, DataFrame
from models import IModel
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
    
    @abstractmethod
    def LoadSavedState():
        """Collect all data saved in data source and instantiate adjacent model objects
        """
        raise RuntimeError


class DatabaseHandler(IDataSource):
    def __init__(self, connectionString: str, tableCreators: Iterable[IModel],
                 engine: SupportedDbEngines = SupportedDbEngines.SQLite) -> None:
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
        self.tableCreators = tableCreators


    def checkIntegrity(self, additionalSetup: Iterable[str]) -> bool:
        """Searches if database contains expected tables, eventually creates missing tables

        Args:
            expected (Iterable[IModel]): IModels with tableName, on missing table also getCreateTableString()
            additionalSetup (Iterable[str]): Queries with steps to perform if found missing tables

        Returns:
            bool: if found intact database
        """
        if self.dbEngineInstance.checkIntegrity(self.tableCreators) == False:
            self.dbEngineInstance.createDatabase(self.tableCreators, additionalSetup)
            return False
        return True
        
    
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

    def LoadSavedState(self) -> None:
        """Collect all data saved in data source and instantiate adjacent model objects
        """
        for tC in self.tableCreators:
            self.SetQuery(f"EXEC {tC.tableName}_load;")
            result = self.GetData()
            for readObj in result:
                tC(**readObj)
    

    def GetData(self) -> str:
        # TODO pewnie będzie trzeba dopisać później na mniejsze fetche
        assert self.query != ""
        
        result = self.dbEngineInstance.FetchAll(self.query)
        
        self.query = ""
        self.parameters = []
        
        return result
    


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