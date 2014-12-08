import sys
from PyQt4.QtGui import *


class NewDatabase(QWidget):
    
    def __init__(self):
        
        super().__init__()
        

        self.showDialog()
        
    def showDialog(self):
        
        text, ok = QInputDialog.getText(self, 'New Database', 
            'Database Name:')
        
        if ok:
            print(text)



if __name__ == "__main__":
    
    
    app = QApplication(sys.argv)
    NewDatabase()
    sys.exit(app.exec_())
