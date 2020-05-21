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

class Tabs(QTabWidget):
    '''Used to create the parts and labor tabs on the main template
    '''
    def __init__(self,job_number):
        super().__init__()
        self.init()
        self.setWindowTitle('BEI Invoice Number {}'.format(job_number))
    def init(self):
        '''Calls the initialization of the parts and labor tabs
        '''
        self.parts()
        self.addTab(self.parts_tab,'Parts Entry')
        self.labor()
        self.addTab(self.labor_tab,'Labor Entry')
        
#        self.find_row=QTimer(self)
#        self.find_row.timeout.connect(self.row_)
#        self.find_row.start(1000)
        #defining it for later
        self.previous_row=int
        self.maximum_row=0
    def parts(self):
        '''Widget for the parts tab
        '''
        self.parts_tab=QWidget()
        self.parts_table=Table(500,7)
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

        self.p_layout=QGridLayout()
        self.p_layout.addWidget(self.parts_table,0,0)
#        self.p_layout.addWidget(self.totals_table,0,1)
        self.parts_tab.setLayout(self.p_layout)
        
    def labor(self):
        '''Widget for the labor tabs

            How it will work:
                1.) Open 'Changable_Documents/Labor_Rates.csv'
                2.) Read the document in and get the names out of it
                3.) Create a dictionary with the names tied to an 
                    instantiation of the tabs_technicain
                4.) Go through and add set the layouts up 
        '''
        #get the current working directory and navigate to the correct folder
        directory=str(Path(os.path.join(os.path.join(os.environ['USERPROFILE']
                    ,'BEI_Invoices')),'Basic_Information_Totals'))
        tech_data=open(str(Path(os.path.join(directory,'Labor_Rates.csv')))
                    ,'r')
        information=tech_data.readlines()
        tech_data.close()
        #add the tech names to a list to be used for keys in a the dictionary
        tech_names=[i.split(sep=',')[0] for i in information]
        self.technicians=QTabWidget(self)
        #set up the tab for each technician
        self.technicians.addTab(Labor_Setup().labor_table,'Butch')
        self.technicians.addTab(Labor_Setup().labor_table,'David')
        self.technicians.addTab(Labor_Setup().labor_table,'Alan')
        self.technicians.addTab(Labor_Setup().labor_table,'Hanna')

#        the main widget instantiated for the labor tab
        self.labor_tab=QWidget()
        self.total_layout=QVBoxLayout()
        self.total_layout.addWidget(self.technicians)
        self.labor_tab.setLayout(self.total_layout)
        
    def keyPressEvent(self, event):
        key = event.key()
        print('here')
        if key == Qt.Key_Return or key == Qt.Key_Enter:
            try:
                for currentQTableWidgetItem in self.parts_table.tableWidget.selectedItems():
                    self.current_row=currentQTableWidgetItem.row()
                if self.current_row!=self.previous_row:
                    self.parts_table.tableWidget.setCurrentCell(self.current_row+1,0)
                    self.calculate(self.current_row)
                self.previous_row=self.current_row
                try:
                    #finding the maximum row
                    float(self.parts_table.tableWidget.item(self.current_row,3).text())
                    self.maximum_row=self.current_row
                except:
                    self.maximum_row=self.maximum_row
            except:
                pass
        else:
            super(Tabs, self).keyPressEvent(event)
        
#    def row_(self):
#        '''Determine the current row
#        '''
#        try:
#            for currentQTableWidgetItem in self.parts_table.tableWidget.selectedItems():
#                self.current_row=currentQTableWidgetItem.row()
#            if self.current_row!=self.previous_row:
#                self.parts_table.tableWidget.setCurrentCell(self.current_row+1,0)
#                self.calculate(self.current_row)
#            self.previous_row=self.current_row
#        except:
#            pass
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
        except:
            pass
    
if __name__=='__main__':
    app=QApplication(sys.argv)
    wid=Tabs()
    sys.exit(app.exec_())