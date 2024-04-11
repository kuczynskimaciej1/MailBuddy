from enum import Enum
import models
from models import __all__ as modelClassNames
from DataSources.dataSources import DatabaseHandler
from pathlib import Path
import json

class ExportLocation(Enum):
    Database = 1
    JSON = 2
    # XML = 3
    # CSV = 4

class ConfigExporter():
    def __init__(self, export: ExportLocation, location: any = None) -> None:
        """Use class methods to instantiate ConfigExporter

        Args:
            export (ExportLocation): used by factory methods
            location (any, optional): used by factory methods. Defaults to None.
        """
        assert location != None
        
        self.export = export
        self.location = location
    
    @classmethod
    def ToDatabase(cls, dbHandler: DatabaseHandler):
        """Binds DatabaseHandler, which will be used to execute export

        Args:
            dbHandler (DatabaseHandler): _description_

        Returns:
            _type_: _description_
        """
        return cls(ExportLocation.Database, dbHandler)
    
           
    @classmethod
    def ToJSON(cls, filename: str):
        return cls(ExportLocation.JSON, filename)
    
    def Export(self):
        match self.export:
            case ExportLocation.Database:
                assert isinstance(self.location, DatabaseHandler)
                #TODO
                
            case ExportLocation.JSON:
                assert isinstance(self.location, str)
                ConfigExporter.saveFile(ConfigExporter.__serializeJsonModelObjects(), self.location)
    
    @staticmethod
    def __serializeJsonModelObjects() -> list:
        result = {}
        classes = modelClassNames
        
        for modelType in classes:
            concreteIModel = getattr(models, modelType)
            try:
                tmp_instances = concreteIModel.all_instances
                if len(tmp_instances) > 0:
                    # This should work as long as there are simple classes
                    # _sa_instance_state is related to declarative_base inheritance, its not needed in our context
                    result[concreteIModel.__tablename__] = [{k: v for k, v in i.__dict__.items() if k != '_sa_instance_state'} for i in tmp_instances]
            except AttributeError as e:
                print(e)
                continue
        
        return result
    
    
    def saveFile(input: dict, location: str) -> None:
        try:
            with open(location, "x", encoding="UTF-8") as f:
                json.dump(input, f, indent=4)
        except Exception as e:
            print(f"Error: {e}")
            raise e
