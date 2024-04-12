from abc import ABCMeta, abstractmethod
from collections.abc import Iterable
from enum import Enum
from pandas import read_csv, read_excel, DataFrame
import models
import sqlalchemy as alchem
import sqlalchemy.orm as orm

class SupportedDbEngines(Enum):
    SQLite=1

class IDataSource():
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


class DatabaseHandler(IDataSource):
    def __init__(self, connectionString: str, tableCreators: Iterable[models.IModel],
                 engine: SupportedDbEngines = SupportedDbEngines.SQLite) -> None:
        """
        Initializes handler, allowing query execution on provided server
        """
        match engine:
            case SupportedDbEngines.SQLite:
                self.dbEngineInstance = alchem.create_engine(connectionString)
            case _:
                raise NotImplementedError
        self.tableCreators = tableCreators


    def checkIntegrity(self) -> bool:
        """Searches if database contains expected tables, eventually creates missing tables

        Args:
            expected (Iterable[IModel]): IModels with tableName, on missing table also getCreateTableString()
            additionalSetup (Iterable[str]): Queries with steps to perform if found missing tables

        Returns:
            bool: if found intact database
        """
        dbIntact = True
        
        md = alchem.MetaData()
        md.reflect(bind=self.dbEngineInstance)
        existing_tables = md.tables.keys()
        expected = [cl.__tablename__ for cl in self.tableCreators]
        missing_tables = set(expected) - set(existing_tables)
        
        if missing_tables:
            print(f"The following tables are missing in the database: {', '.join(missing_tables)}")
            self.instantiateClasses(missing_tables)
            dbIntact = False
        return dbIntact


    def instantiateClasses(self, missing_tables: list[str] | list[models.IModel]) -> None:
        # if len(additionalSetup) != 0:
        
        #     # DEBUG
        #     md = alchem.MetaData()
        #     md.reflect(bind=self.dbEngineInstance)
        #     existing_tables = md.tables.keys()
            
            
        #     for table_name in missing_tables:
        #         tableClass = next((cl for cl in additionalSetup if cl.name == table_name), None)
        #         tableClass.metadata.create_all(self.dbEngineInstance)
        #     return
        
        for table_name in missing_tables:
            if isinstance(table_name, str):
                table_name = next((cl for cl in self.tableCreators if cl.__tablename__ == table_name), None)
            
            table_name.__table__.create(self.dbEngineInstance)
            # raise AttributeError(f"{table_name} is not name of table or IModel subclass")
            

    def LoadSavedState(self) -> None:
        """Collect all data saved in data source and instantiate adjacent model objects
        """
        with orm.Session(self.dbEngineInstance) as session:
            for tC in self.tableCreators:
                try:
                    result = session.execute(alchem.select(tC)).all()
                    for readObj in result:
                        tC(**readObj)
                except Exception as e:
                    print(e)
                    continue


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