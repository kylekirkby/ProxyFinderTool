
from PyQt4.QtSql import *
import sqlite3

class SQLConnection:
    
    """Handles the conncetion to the SQL database"""
    
    def __init__(self,path):

        self.path = path

        self.db = None
        
    def create_database(self):
        with sqlite3.connect(self.path) as db:
            cursor = db.cursor()
            sql = """ CREATE TABLE Proxies(
                    ProxyID integer,
                    ProxyIP text,
                    ProxyPort text,
                    ProxyConnectionType text,
                    ProxySpeed text,
                    ProxyType text,
                    ProxyCountry text,
                    ProxyCity text,
                    Primary Key(ProxyID));
                    """

            self.create_table("Proxies",sql)
            

        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName(self.path)

        opened_ok = self.db.open()

        return opened_ok

    
    def create_table(self,table_name,sql):
        
        with sqlite3.connect(self.path) as db:
            cursor = db.cursor()
            cursor.execute("select name from sqlite_master where name=?",(table_name,))
            result = cursor.fetchall()
            if len(result) == 1:
                pass
            else:
                cursor.execute(sql)
                db.commit()

    def open_database(self):
        
        if self.db:
            self.close_database()

        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName(self.path)

        opened_ok = self.db.open()

        return opened_ok
    
    def close_database(self):

        if self.db:
            if self.db.isOpen() == True:
                self.db.close()
                #remove the database from the QSqlDatabase object - "conn" is the default
                #database name
                QSqlDatabase.removeDatabase("conn")
                closed = self.db.open()
                print("closed con")
                self.db = None
            else:
                print("No connection open")
        else:
            print("No connection to close!")

            

                
    def numberOfProxies(self):
        
        query = QSqlQuery()
        query.prepare(""" SELECT * FROM Proxies """)
        query.exec_()

        return query.size()

    def getAllProxies(self):

        query = QSqlQuery()
        query.prepare("SELECT * FROM Proxies")
        query.exec_()

        
        results = []

        header = self.selected_columns
         
        query.first()
         
        while query.isValid():
            record = [query.value(index).toString() for index in range(len(header))]
            results.append(record)
            query.next()

        print(results)
        
            
    def addProxy(self, proxy):
        
        query = QSqlQuery()
        
        query.prepare("""INSERT INTO Proxies(ProxyIP,ProxyPort,ProxyConnectionType,
ProxySpeed,ProxyType,ProxyCountry,ProxyCity) VALUES(:ip,:port,:connType,
:speed,:type,:country,:city)""")

        proxyAddr = proxy[0]
        proxyAddrSplit = proxyAddr.split(":")
        proxyIP = proxyAddrSplit[0]
        proxyPort = proxyAddrSplit[1]
        proxyConnection = proxy[1]
        proxySpeed = proxy[2]
        proxyType = proxy[3]
        proxyCountry = proxy[4]
        proxyCity = proxy[5]
        
        query.bindValue(":ip",proxyIP)
        query.bindValue(":port",proxyPort)
        query.bindValue(":connType",proxyConnection)
        query.bindValue(":speed",proxySpeed)
        query.bindValue(":type",proxyType)
        query.bindValue(":country",proxyCountry)
        query.bindValue(":city",proxyCity)

        query.exec_()
                
    def closeEvent(self,event):
        
        self.close_database()

    def show_all_products(self):
        query = QSqlQuery()
        query.prepare(""" SELECT * FROM Product""")
        query.exec_()
        return query

    def find_products_by_number(self,values):
        
        query = QSqlQuery()
        query.prepare(""" SELECT * FROM Product WHERE ProductID =? """)
        query.addBindValue(values[0])
        query.exec_()
        return query
