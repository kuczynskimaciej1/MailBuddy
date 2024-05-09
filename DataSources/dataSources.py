from __future__ import annotations
from abc import ABCMeta, abstractmethod
from collections.abc import Iterable
from enum import Enum
from pandas import read_csv, read_excel, DataFrame
from additionalTableSetup import GroupContacts
from models import IModel, Contact
import sqlalchemy as alchem
import sqlalchemy.orm as orm
from sqlalchemy.ext.hybrid import hybrid_property

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
    def __init__(self, connectionString: str, tableCreators: Iterable[IModel],
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

    def GetData(self, type: IModel, **kwargs) -> list:
        Session = orm.sessionmaker(bind=self.dbEngineInstance)
        with Session() as session:
            try:
                if len(kwargs) > 0:
                    selectionResult = session.query(type).filter_by(**kwargs).all()
                else:
                    selectionResult = session.query(type).all()
            finally:
                session.close()
        self.dbEngineInstance.dispose()
        return selectionResult


    def instantiateClasses(self, missing_tables: list[str] | list[IModel]) -> None:
        for table_name in missing_tables:
            if isinstance(table_name, str):
                table_name = next((cl for cl in self.tableCreators if cl.__tablename__ == table_name), None)
            
            table_name.__table__.create(self.dbEngineInstance)
            

    def LoadSavedState(self) -> None:
        """Collect all data saved in data source and instantiate adjacent model objects
        """
        Session = orm.sessionmaker(bind=self.dbEngineInstance)
        with Session() as session:
            for tC in self.tableCreators:
                try:
                    #TODO to pewnie będzie do poprawy przy zapisywaniu innych obiektów
                    result = session.execute(alchem.select(tC)).all()
                    if len(result) == 0: continue
                    for readObj in result:
                        toinit = readObj[0].__dict__
                        tC(**toinit)
                except Exception as e:
                    print(e)
                    continue
        IModel.run_loading = False

    def Save(self, obj: IModel | GroupContacts):
        Session = orm.sessionmaker(bind=self.dbEngineInstance)
        with Session() as session:
            session.add(obj)
            session.commit()
            session.refresh(obj)
        self.dbEngineInstance.dispose()

    def DeleteEntry(self, obj: IModel | GroupContacts):
        Session = orm.sessionmaker(bind=self.dbEngineInstance)
        with Session() as session:
            session.delete(obj)
            session.commit()

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


class CSVHandler(IDataSource):
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
        
    @staticmethod
    def ParseTo(dataFrameSlice: DataFrame):
        pass

class GapFillSource():
    all_instances: list[GapFillSource] = []
    
    def __init__(self, source: IDataSource | IModel = Contact) -> None:
        if isinstance(source, IDataSource):
            self.iData: IDataSource = source
        elif issubclass(source, IModel):
            self.model_source: IModel = source
        else:
            raise AttributeError(f"Got {type(source)}, which is not IDataSource or IModel implementation")
        self.possible_values: dict[str, str] = None
        GapFillSource.all_instances.append(self)
        self.get_possible_values()
        
    def get_possible_values(self):
        if hasattr(self, "iData"):
            idata_type = type(self.iData)
            match(idata_type):
                case type(DatabaseHandler):
                    # openTablePicker()
                    pass
                case type(XLSXHandler):
                    # openSheetPicker()
                    pass
                case type(CSVHandler):
                    # openCsvPicker()
                    pass
        elif hasattr(self, "model_source"):
            if self.model_source == Contact:
                self.possible_values = { name: attr for name, attr in Contact.__dict__.items() if isinstance(attr, hybrid_property) and attr != "all_instances" }
            else:
                raise AttributeError(f"{type(self.model_source)} isn't supported")
