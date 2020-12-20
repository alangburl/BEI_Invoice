#tab widget used to create the working window of the parts and labor
#imports from other scripts for the purpose fo spliting the file size up
from tabs_technicians import Labor_Setup
#prefined imports
import sys,os
from pathlib import Path
from PyQt5.QtWidgets import (QApplication, QPushButton,QWidget,QGridLayout,
                             QSizePolicy,QTabWidget,QHeaderView,
                             QTableWidgetItem,QVBoxLayout)
from PyQt5.QtCore import pyqtSignal,Qt

class Labor_Tabs(QWidget):
    '''Used to create the labor tabs on the main template
    '''
    previous_row=int
    labor_total=pyqtSignal(float)
    def __init__(self,job_number,font):
        super().__init__()
        self.font=font
        self.init()
        self.setWindowTitle('BEI Invoice Number {}'.format(job_number))
    def init(self):
        '''Calls the initialization of the labor tabs
        '''
        self.labor()
#        self.addTab(self.labor_tab,'Labor Entry')
        self.previous_row=int
        self.maximum_row=0

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
        self.hourly_wage={}
        tech_names=[]
        for i in range(len(information)):
            tech_names.append(information[i].split(sep=',')[0])
            self.hourly_wage[i]=[float(information[i].split(sep=',')[1]),
                             float(information[i].split(sep=',')[2])]
            
        self.technicians=QTabWidget(self)
        #set up the tab for each technician
        self.t0=Labor_Setup(self.font).labor_table
        self.t1=Labor_Setup(self.font).labor_table
        self.t2=Labor_Setup(self.font).labor_table
        self.t3=Labor_Setup(self.font).labor_table
        self.t4=Labor_Setup(self.font).labor_table
        self.t5=Labor_Setup(self.font).labor_table
        self.t6=Labor_Setup(self.font).labor_table
        self.t7=Labor_Setup(self.font).labor_table
        self.t_tabs=[self.t0,self.t1,self.t2,self.t3,
                     self.t4,self.t5,self.t6,self.t7]
        for i in range(len(tech_names)):
            self.technicians.addTab(self.t_tabs[i],tech_names[i])
        for j in range(len(tech_names),len(self.t_tabs)):
            self.t_tabs[j].close()
#        self.technicians.addTab(self.t1,'David')
#        self.technicians.addTab(self.t2,'Alan')
#        self.technicians.addTab(self.t3,'Hanna')
        
        self.counts=self.technicians.count()

        self.total_layout=QVBoxLayout()
        self.total_layout.addWidget(self.technicians)
        self.setLayout(self.total_layout)
        
    def keyPressEvent(self, event):
        key = event.key()
        operator=self.t0
        if key == Qt.Key_Return or key == Qt.Key_Enter:
            try:
                index=self.technicians.currentIndex()
                operator=self.determine_tech(index)
                    
                for cqt in operator.tableWidget.selectedItems():
                    current_row=cqt.row()
    #            if current_row!=self.previous_row:
                operator.tableWidget.setCurrentCell(current_row+1,0)
                self.calculate(current_row,operator,index)
    #            self.previous_row=current_row
            except:
                pass
        else:
            super(Labor_Tabs, self).keyPressEvent(event)

    def calculate(self,row,current_tech,index):
        '''Calculate the overtime and regular time for the current row
        '''
        try:
            regular_hours=float(current_tech.tableWidget.item(row,3).text())
        except:
            regular_hours=0
        try:
            ot_hours=float(current_tech.tableWidget.item(row,4).text())
        except:
            ot_hours=0
        try:
            hours_wage=float(current_tech.tableWidget.item(row,5).text())
        except:
            hours_wage=self.hourly_wage[index][0]
        try:
            ot_hours_wage=float(current_tech.tableWidget.item(row,6).text())
        except:
            ot_hours_wage=self.hourly_wage[index][1]
        labor_t=regular_hours*hours_wage+ot_hours*ot_hours_wage
        current_tech.tableWidget.setItem(row,7,QTableWidgetItem(str(labor_t)))
        total=self.find_tech_total(index)
        self.labor_total.emit(total)
        
    def find_tech_total(self,index):
        '''Sum up the total amount for the specified tech
        '''
        operator=self.determine_tech(index)
        total=0   
        for i in range(100):
            try:
                total+=float(operator.tableWidget.item(i,7).text())
            except:
                break  
        return total
    
    def find_tech_individual(self):
        '''
        Find the individual tech labor contribution
        '''
        totals=[]
        for i in range(self.counts):
            totals.append(self.find_tech_total(i))
        return totals
        
    def read_data_out(self,index):
        operator=self.determine_tech(index)
        
        labor_data=[]
        for i in range(100):
            try:
                row=[]
                for j in range(8):
                    try:
                        float(operator.tableWidget.item(i,7).text())
                        if j==2:
                            row.append(operator.tableWidget.item(i,j).text().replace(',','.'))
                        else:
                            row.append(operator.tableWidget.item(i,j).text())
                    except:
                        row.append('')
                labor_data.append(row)
            except:
                break
        return labor_data
    
    def read_in_data(self,index,data):
        operator=self.determine_tech(index)
        
        for i in range(len(data)):
            for j in range(len(data[i])):
                if data[i][j]!='':
                    operator.tableWidget.setItem(i,j,
                                                 QTableWidgetItem(data[i][j]))
        
    def determine_tech(self,index):
        operator=self.t_tabs[index]
#        if index==0:
#            operator=self.t0
#        elif index==1:
#            operator=self.t1
#        elif index==2:
#            operator=self.t2
#        elif index==3:
#            operator=self.t3
        return operator
        
        
if __name__=='__main__':
    app=QApplication(sys.argv)
    wid=Labor_Tabs(123)
    sys.exit(app.exec_())