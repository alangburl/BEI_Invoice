from table_widget import Table
#prefined imports
import sys,os
from PyQt5.QtWidgets import (QApplication, QTableWidgetItem,QWidget,
                             QPushButton,QVBoxLayout)
from PyQt5.QtGui import QFont,QIcon, QImage, QPalette, QBrush

class Labor_Rates(QWidget):
    def __init__(self,base_directory,font,size_policy):
        super().__init__()
        self.base=base_directory
        self.rates=Table(6,3,font)
        self.rates.tableWidget.setHorizontalHeaderItem(0,
                                                   QTableWidgetItem('Name'))
        self.rates.tableWidget.setHorizontalHeaderItem(1,
                                           QTableWidgetItem('Regular Rate'))
        self.rates.tableWidget.setHorizontalHeaderItem(2,
                                           QTableWidgetItem('Overtime Rate'))  
        self.save=QPushButton('Save',self)
        self.save.setFont(font)
        self.save.setSizePolicy(size_policy,size_policy)
        self.save.clicked.connect(self.write_data)
        layout=QVBoxLayout(self)
        layout.addWidget(self.rates)
        layout.addWidget(self.save)
        self.setLayout(layout)
        self.read_data()
        self.setWindowTitle('Change Labor Rates')
        self.setWindowIcon(QIcon('BEI_Logo.png'))
        backimage=QImage('BEI_Logo.png')
        palette=QPalette()
        palette.setBrush(10,QBrush(backimage))
        self.setPalette(palette)
#        self.show()
        
    def read_data(self):
        '''Read the current data and display it on the table
        '''
        self.files=os.path.join(os.path.join(self.base,'Basic_Information_Totals'),
                          'Labor_Rates.csv')
        f=open(self.files,'r')
        data=f.readlines()
        f.close()
        self.names=[]
        self.regular=[]
        self.ot=[]
        for i in range(len(data)):
            self.names.append(data[i].split(sep=',')[0])
            self.regular.append(data[i].split(sep=',')[1])
            self.ot.append(float(data[i].split(sep=',')[2]))
        #put the data into the table
        for i in range(len(self.names)):
            self.rates.tableWidget.setItem(i,0,
                                          QTableWidgetItem(self.names[i]))
            self.rates.tableWidget.setItem(i,1,
                                          QTableWidgetItem(self.regular[i]))
            self.rates.tableWidget.setItem(i,2,
                                          QTableWidgetItem(str(self.ot[i])))
    def write_data(self):
        '''Read the data out of each cell and write it to the file
        '''
        f=open(self.files,'w')
        for i in range(len(self.names)):
            f.write('{},{},{}\n'.format(self.rates.tableWidget.item(i,0).text(),
                    self.rates.tableWidget.item(i,1).text(),
                    self.rates.tableWidget.item(i,2).text()))
        f.close()
        self.close()
            