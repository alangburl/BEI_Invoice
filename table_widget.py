import sys
from PyQt5.QtWidgets import (QMainWindow, QApplication, QWidget, 
                             QAction, QTableWidget,QTableWidgetItem,
                             QVBoxLayout,QHeaderView,QSizePolicy)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot,Qt

class Table(QWidget):
    '''Create the tables necessary for parts and labor
    '''
    def __init__(self,rows,columns,font):
        super().__init__()
#        self.showMaximized()
        self.font=font
        self.rows=rows
        self.columns=columns
        self.size_policy=QSizePolicy.Expanding
        self.init()
        self.show()
        
    def init(self):
        '''initialize all the necessary widgets for the table
        '''
        self.table_init()        
        self.layout=QVBoxLayout(self)
        self.layout.addWidget(self.tableWidget)
        self.setLayout(self.layout)
        
    def table_init(self):
        '''Initialize the table entry area
        '''
        self.tableWidget=QTableWidget(self)
        self.tableWidget.setRowCount(self.rows)
        self.tableWidget.setColumnCount(self.columns)
        self.tableWidget.setSizePolicy(self.size_policy,self.size_policy)
        self.tableWidget.setFont(self.font)
        self.tableWidget.horizontalHeader().setFont(self.font)
        self.tableWidget.horizontalHeader(
                ).setSectionResizeMode(QHeaderView.ResizeToContents)
            
if __name__=='__main__':
    app = QApplication(sys.argv)
    ex = Table()
    sys.exit(app.exec_())