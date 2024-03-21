import sqlite3
from typing import Optional, Iterable
from models import IModel

class sqlite():
    
    def __init__(self, databaseName: str):
        self.dbName = databaseName
        self.connection = sqlite3.connect(self.dbName)
        
    def checkIntegrity(self, tableCreators: Iterable[IModel], ) -> bool:
        con = sqlite3.connect(self.dbName)
        cur = con.cursor()
        
        existingTables = cur.execute("SELECT name FROM sqlite_schema WHERE type ='table' AND name NOT LIKE 'sqlite_%';").fetchall()
        
        for classType in tableCreators:
            if classType.getTableName() not in [table[0] for table in existingTables]:
                return False
            
        return True
    
    def createDatabase(self, tableCreators: Iterable[IModel], additionalSetup: Optional[Iterable[str]] = []):
        con = sqlite3.connect(self.dbName)
        cur = con.cursor()

        print("TableCreators: " + str(tableCreators))
        for modelClass in tableCreators:
            cmd = modelClass.getCreateTableString()
            if (cmd != None):
                cur.execute(cmd)

        for cmd in additionalSetup:
            cur.execute(cmd)
        
        con.commit()

    def FetchAll(self, query: str) -> Optional[str]:
        c = self.connection.cursor()
        result = c.execute(query)
        return result.fetchall()
