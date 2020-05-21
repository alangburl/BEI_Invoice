#tab widget used to create the working window of the parts and labor
#imports from other scripts for the purpose fo spliting the file size up
from table_widget import Table
from tabs_technicians import Labor_Setup
#prefined imports
import sys,os
from pathlib import Path
from PyQt5.QtWidgets import (QApplication, QPushButton,QWidget,QGridLayout,
                             QSizePolicy,QTabWidget,QHeaderView,
                             QTableWidgetItem,QVBoxLayout)
from PyQt5.QtGui import QFont,QIcon, QImage, QPalette, QBrush
from PyQt5.QtCore import QThread, pyqtSignal, QTimer,Qt

class Parts_Tabs(QWidget):
    '''Used to create the parts and labor tabs on the main template
    '''
    parts_total=0
    freight_total=0
    total=pyqtSignal(float)
    def __init__(self,job_number):
        super().__init__()
        self.init()
        self.setWindowTitle('BEI Invoice Number {}'.format(job_number))
    def init(self):
        '''Calls the initialization of the parts and labor tabs
        '''
        self.parts()
#        self.addTab(self.parts_tab,'Parts Entry')
        self.previous_row=int
        self.maximum_row=0
#        self.parts_total=0
    def parts(self):
        '''Widget for the parts tab
        '''
        self.parts_table=Table(500,8)
        self.parts_table.tableWidget.setHorizontalHeaderItem(
                0,QTableWidgetItem('Qty.'))
        self.parts_table.tableWidget.setHorizontalHeaderItem(
                1,QTableWidgetItem('Part Number'))
        self.parts_table.tableWidget.setHorizontalHeaderItem(
                2,QTableWidgetItem('Description'))
        self.parts_table.tableWidget.setHorizontalHeaderItem(
                3,QTableWidgetItem('Cost'))
        self.parts_table.tableWidget.setHorizontalHeaderItem(
                4,QTableWidgetItem('Price'))
        self.parts_table.tableWidget.setHorizontalHeaderItem(
                5,QTableWidgetItem('Extension'))
        self.parts_table.tableWidget.setHorizontalHeaderItem(
                6,QTableWidgetItem('Freight')) 
        self.parts_table.tableWidget.setHorizontalHeaderItem(
                7,QTableWidgetItem('Misc.')) 

        self.parts_table.tableWidget.verticalHeader(
                ).setSectionResizeMode(QHeaderView.ResizeToContents)
        self.parts_table.tableWidget.horizontalHeader(
                ).setSectionResizeMode(QHeaderView.Interactive)
        self.parts_table.tableWidget.horizontalHeader().resizeSection(2,300)
        self.p_layout=QGridLayout()
        self.p_layout.addWidget(self.parts_table,0,0)
        self.setLayout(self.p_layout)

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_Return or key == Qt.Key_Enter:
            try:
                for currentQTableWidgetItem in self.parts_table.tableWidget.selectedItems():
                    self.current_row=currentQTableWidgetItem.row()
                self.parts_table.tableWidget.setCurrentCell(self.current_row+1,0)
                self.calculate(self.current_row)
            except:
                pass
        elif key==Qt.Key_Delete:
            for currentQTableWidgetItem in self.parts_table.tableWidget.selectedItems():
                current_row=currentQTableWidgetItem.row()
            try:
                self.parts_table.tableWidget.removeRow(current_row)
            except:
                pass
            for i in range(500):
                try:
                    float(self.parts_table.tableWidget.item(i,0).text())
                    self.calculate(i)
                except:
                    break
        else:
            super(Parts_Tabs, self).keyPressEvent(event)

    def calculate(self,current_row):
        '''Calculate the mark up and put it in the correct cells
        '''
        qty=float
        cost=float
        price=0.0
        exten=0.00
        '''subject to be changed by a user input'''
        multiplier=0.2
        #try and calculate the mark up, otherwise, leave it alone
        try:
            if self.parts_table.tableWidget.item(current_row,0).text()!='*':
                qty=float(self.parts_table.tableWidget.item(current_row,0).text())
                cost=float(self.parts_table.tableWidget.item(current_row,3).text())
                if qty==1:
                    exten=-cost/(multiplier-1)
                    self.parts_table.tableWidget.setItem(
                            current_row,5,QTableWidgetItem(str(round(exten,2))))
                    self.parts_table.tableWidget.setItem(
                            current_row,4,QTableWidgetItem(0))
                else:
                    price=-cost/(multiplier-1)
                    exten=price*qty
                    self.parts_table.tableWidget.setItem(
                            current_row,4,QTableWidgetItem(str(round(price,2))))
                    self.parts_table.tableWidget.setItem(
                            current_row,5,QTableWidgetItem(str(round(exten,2))))
            else:
                True
        except:
            True
        #find the new total for all the cells
        self.parts_sumation()
        
    def parts_sumation(self):
        self.parts_total=0
        self.freight_total=0
        for i in range(100):
            try:
                if self.parts_table.tableWidget.item(i,0).text()!='*':
                    self.parts_total+=float(
                        self.parts_table.tableWidget.item(i,5).text())
                    try:
                        self.freight_total+=float(
                            self.parts_table.tableWidget.item(i,6).text())
                    except:
                        self.freight_total+=0
                else:
                    self.parts_total+=0
                    self.freight_total+=0
            except:
                break
        self.total.emit(self.parts_total)
        
    def read_in_data(self,data):
        '''Take the data given and place it in the appropriate cells
        '''
        self.freight_total=0
        for i in range(len(data)):
            for j in range(len(data[i])):
                if ''!=data[i][j]:
                    self.parts_table.tableWidget.setItem(i,j,
                                                 QTableWidgetItem(data[i][j]))
    
if __name__=='__main__':
    app=QApplication(sys.argv)
    wid=Parts_Tabs(123)
    sys.exit(app.exec_())