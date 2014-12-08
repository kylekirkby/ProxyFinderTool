from PyQt4.QtCore import *
from PyQt4.QtGui import *

import sys

from NewDatabase import *
from SQLConnection import *
from proxy import  *

class MainWindow(QMainWindow):

    """ This is the Main Window class for the proxy finder tool. """

    def __init__(self):

        super().__init__()


        self.setWindowTitle("Proxy Finder Tool")

        self.resize(250,300)


        #Attached SQL Connection
        self.connection = None

        self.icon = QIcon(QPixmap("./globe.png"))
        self.setWindowIcon(self.icon)

        self.mainSettings()
        

        self.stacked_layout = QStackedLayout()

        self.mainLayout()

        self.connections()
        
        self.widget = QWidget()
        self.widget.setLayout(self.stacked_layout)

        self.setCentralWidget(self.widget)

    def mainSettings(self):
        

        self.refreshButton = QPushButton("Refresh")
        self.exportList = QPushButton("Save List")

        self.statusBar = QStatusBar()

        self.setStatusBar(self.statusBar)
        
        self.menuBar = QMenuBar()

        #menus for the main menu bar
        self.databaseMenu  = self.menuBar.addMenu("Database")
        self.proxyMenu  = self.menuBar.addMenu("Proxies")
        self.helpMenu = self.menuBar.addMenu("Help")
        

        #actions
        self.getList = QAction("Get List", self)
        self.saveList = QAction("Save List", self)
        

        self.openDatabase = QAction("Open Database", self)
        self.newDatabase = QAction("New Database", self)
        self.closeDatabase = QAction("Close Database", self)
        self.closeDatabase.setEnabled(False)

        self.about = QAction("About", self)

        #add actions to menus
        self.proxyMenu.addAction(self.getList)
        self.proxyMenu.addAction(self.saveList)

        self.databaseMenu.addAction(self.newDatabase)
        self.databaseMenu.addAction(self.openDatabase)
        self.databaseMenu.addAction(self.closeDatabase)

        self.helpMenu.addAction(self.about)
    
        #set the menu bar
        self.setMenuBar(self.menuBar)

    def mainLayout(self):

        #this is the main initial layout
        self.resultsTable = QListWidget()


        #current database

        self.currentDatabase = QLabel("Current Database: ")
        self.databaseNameLabel = QLabel("None")

        self.currentDbLayout = QHBoxLayout()
        self.currentDbLayout.addWidget(self.currentDatabase)
        self.currentDbLayout.addWidget(self.databaseNameLabel)

        self.currentDbWidget = QWidget()
        self.currentDbWidget.setLayout(self.currentDbLayout)

        #buttons

        self.btnLayout = QHBoxLayout()


        self.getListBtn = QPushButton("Get List")
        self.saveListBtn = QPushButton("Save List")
        self.exportListBtn = QPushButton("Export List")
        
        self.btnLayout.addWidget(self.getListBtn)
        self.btnLayout.addWidget(self.saveListBtn)
        self.btnLayout.addWidget(self.exportListBtn)

        self.btnWidget = QWidget()
        self.btnWidget.setLayout(self.btnLayout)

        # Main Layout

        self.mainVertical = QVBoxLayout()
        self.mainVertical.addWidget(self.currentDbWidget)
        self.mainVertical.addWidget(self.resultsTable)
        self.mainVertical.addWidget(self.btnWidget)

        self.disableProxies()
        # Main Widget
        
        self.mainWidget = QWidget()
        self.mainWidget.setLayout(self.mainVertical)


        #Add to Stacked Layout
        self.stacked_layout.addWidget(self.mainWidget)

    def createNewDatabase(self):

        path = QFileDialog.getSaveFileName()

        if self.connection:
            self.connection.close_database()
            
        self.connection = SQLConnection(path)
        self.connection.create_database()
        
        self.databaseNameLabel.setText(path)

        
        self.closeDatabase.setEnabled(True)
        self.openDatabase.setEnabled(False)
        self.newDatabase.setEnabled(False)

        
        self.statusBar.showMessage("Database has been created.")

        self.enableProxies()

        self.db_open()

    def getProxies(self):
        if self.connection == None:
            self.statusBar.showMessage("No Database Open!")
        else:
            thread = ProxyList()
            thread.complete.connect(self.populate_db)
            thread.start()
        
    def enableProxies(self):
        self.getList.setEnabled(True)
        self.saveList.setEnabled(True)

        self.getListBtn.setEnabled(True)
        self.saveListBtn.setEnabled(True)
        self.exportListBtn.setEnabled(True)

    def populate_db(self, results):
        
        self.statusBar.showMessage("Collecting Data. Please wait...")
            
        for i in range(len(proxies)):
            query = self.connection.addProxy(proxies[i])
            self.statusBar.showMessage("Gathering {0} of {1} proxies.".format(
                    i + 1,len(proxies)))
                
        self.statusBar.showMessage("Gathering Complete!")
        

    def populate_table_init(self):

        numberOfProxies = self.connection.numberOfProxies()

        if num > 0:
            results = self.connection.getAllProxies()
        else:
            self.statusBar.showMessage("No Proxies in Database.")

    def db_open(self):

        numberOfProxies = self.connection.numberOfProxies()
        num = int(numberOfProxies)
        print(num)
        if num > 0:
            self.connection.getAllProxies()
        else:
            self.statusBar.showMessage("No Proxies in Database.")
        


    def disableProxies(self):
        self.getList.setEnabled(False)
        self.saveList.setEnabled(False)

        self.getListBtn.setEnabled(False)
        self.saveListBtn.setEnabled(False)
        self.exportListBtn.setEnabled(False)

    def openDatabaseConn(self):

        self.close_connection()

        path = QFileDialog.getOpenFileName()
        self.connection = SQLConnection(path)        
        opened = self.connection.open_database()

        if opened:
            self.openDatabase.setEnabled(False)
            self.newDatabase.setEnabled(False)
            self.closeDatabase.setEnabled(True)

            self.statusBar.showMessage("Database has been opened.")
            self.databaseNameLabel.setText(path)
            self.enableProxies()
            self.db_open()
        

    def close_connection(self):
        if self.connection:
            self.connection.close_database()
            self.statusBar.showMessage("Database has been closed.")
            self.databaseNameLabel.setText("None")
            
            self.newDatabase.setEnabled(True)
            self.openDatabase.setEnabled(True)
            self.closeDatabase.setEnabled(False)
            
            self.connection = None

            self.disableProxies()
        else:
            self.statusBar.showMessage("No Database to close.")

    def connections(self):

        self.newDatabase.triggered.connect(self.createNewDatabase)
        self.openDatabase.triggered.connect(self.openDatabaseConn)
        self.closeDatabase.triggered.connect(self.close_connection)
        self.getListBtn.clicked.connect(self.getProxies)
        self.getList.triggered.connect(self.getProxies)

        

if __name__ == "__main__":

    
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    window.raise_()
    app.exec_()
