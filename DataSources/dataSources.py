from __future__ import annotations
from collections.abc import Iterable
from enum import Enum
from .dataSourceAbs import IDataSource
from pandas import read_csv, read_excel, DataFrame
from additionalTableSetup import GroupContacts
from group_controller import GroupController
from models import DataImport, Group, IModel, Contact, Template
import sqlalchemy as alchem
import sqlalchemy.orm as orm
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.hybrid import hybrid_property

class SupportedDbEngines(Enum):
    SQLite=1

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
        IDataSource.current_instance = self


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
        self.runAdditionalBindings()
        
    
    def runAdditionalBindings(self):
        for g in Group.all_instances:
            g.contacts = GroupController.get_contacts(g)
        
        for t in Template.all_instances:
            if t.dataimport_id != None:
                for di in DataImport.all_instances:
                    if t.dataimport_id == di.id:
                        t.dataimport = di
                        break # TODO w razie dodanie większej ilości di - templatek
                    

    def Update(self, obj: IModel):
        Session = orm.sessionmaker(bind=self.dbEngineInstance)
        try:
            with Session() as session:
                session.merge(obj)
                session.commit()
        except IntegrityError as ie:
            print(ie)
        except Exception as e:
            print(e)
        finally:
            self.dbEngineInstance.dispose()

    def Save(self, obj: IModel | GroupContacts):
        Session = orm.sessionmaker(bind=self.dbEngineInstance)
        try:
            with Session() as session:
                session.add(obj)
                session.commit()
                session.refresh(obj)
        except IntegrityError as ie:
            print(ie)
        except Exception as e:
            print(e)
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
        # if isinstance(source, IDataSource):
        #     self.iData: IDataSource = source
        # el
        if isinstance(source, DataImport) or isinstance(source, list):
            self.model_source: IModel = source
        elif issubclass(source, IModel):
            self.model_source: IModel = source
        else:
            raise AttributeError(f"Got {type(source)}, which is not IDataSource or IModel implementation")
        self.possible_values: dict[str, str] = None
        GapFillSource.all_instances.append(self)
        self.get_possible_values()
        
    def get_possible_values(self):
        # if hasattr(self, "iData"):
        #     idata_type = type(self.iData)
        #     match(idata_type):
        #         case type(DatabaseHandler):
        #             # openTablePicker()
        #             pass
        #         case type(XLSXHandler):
        #             # openSheetPicker()
        #             pass
        #         case type(CSVHandler):
        #             # openCsvPicker()
        #             pass
        # el
        if hasattr(self, "model_source"):
            if self.model_source == Contact:
                self.possible_values = { name: attr for name, attr in Contact.__dict__.items() if isinstance(attr, hybrid_property) and attr != "all_instances" }
            elif isinstance(self.model_source, DataImport):
                self.possible_values = self.model_source.getColumnPreview()
            else:
                raise AttributeError(f"{type(self.model_source)} isn't supported")
        else:
            raise AttributeError(f"Incorrectly created GapFillSource, expected 'model_source'={self.model_source} to be present.")

    @staticmethod
    def getPreviewText(searched: str) -> str | None:
        for g in GapFillSource.all_instances:
            candidate = g.possible_values.get(searched, None)
            if candidate == None:
                continue
            return candidate
        return None
