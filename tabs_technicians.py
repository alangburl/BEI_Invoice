from table_widget import Table
#prefined imports
import sys
from PyQt5.QtWidgets import (QApplication, QTableWidgetItem,QHeaderView)

class Labor_Setup():   
    def __init__(self,font):
        super().__init__()
        #setting up the necessary stuff for each tech
        self.labor_table=Table(500,8,font)
        self.labor_table.tableWidget.setHorizontalHeaderItem(0,
                                                     QTableWidgetItem('Date'))
        self.labor_table.tableWidget.setHorizontalHeaderItem(1,
                                             QTableWidgetItem('Job Number'))
        self.labor_table.tableWidget.setColumnHidden(1, True)        
        self.labor_table.tableWidget.setHorizontalHeaderItem(2,
                                             QTableWidgetItem('Description'))
        self.labor_table.tableWidget.resizeRowsToContents()
        self.labor_table.tableWidget.setHorizontalHeaderItem(3,
                                             QTableWidgetItem('Hours'))
        self.labor_table.tableWidget.setHorizontalHeaderItem(4,
                                         QTableWidgetItem('Overtime Hours'))
        self.labor_table.tableWidget.setHorizontalHeaderItem(5,
                                     QTableWidgetItem('Hourly Rate Override'))
        self.labor_table.tableWidget.setHorizontalHeaderItem(6,
                             QTableWidgetItem('Overtime Hours\nRate Overide'))
        self.labor_table.tableWidget.setHorizontalHeaderItem(7,
                             QTableWidgetItem('Running Total'))
        self.labor_table.tableWidget.setColumnHidden(7, True)     
        
        self.labor_table.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        self.labor_table.tableWidget.horizontalHeader().resizeSection(2,400)
        self.labor_table.tableWidget.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        
if __name__=='__main__':
    app=QApplication(sys.argv)
    wid=Labor_Setup()
    sys.exit(app.exec_())