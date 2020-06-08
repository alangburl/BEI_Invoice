#a class to update basic invoice values
from PyQt5.QtWidgets import (QWidget,QLineEdit,QPushButton,QGridLayout,QLabel,
                             QInputDialog)
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QIcon
import os,shutil

class Update(QWidget):
    tax=pyqtSignal(float)
    def __init__(self,dire,job_number,font,size_policy):
        self.base_directory=dire
        self.current_job=job_number
        self.font=font
        self.size_policy=size_policy
               #first read in the current status of the basic info
        location=os.path.join(os.path.join(self.base_directory,
                                           'Saved_Invoices'),
                                            '{}'.format(self.current_job))
        e=open(os.path.join(location,'Basic_Info.csv'),'r')
        basic=e.readlines()
        e.close()
        
        self.update_info=QWidget()
        self.update_info.setWindowTitle('Update Basic Information')
        self.update_info.setWindowIcon(QIcon('BEI_Logo.png'))
        mach=QLabel('Machine',self)
        mach.setFont(self.font)
        mach.setSizePolicy(self.size_policy,self.size_policy)
        
        tax=QLabel('Tax [%]',self)
        tax.setFont(self.font)
        tax.setSizePolicy(self.size_policy,self.size_policy)
        
        self.machine=QLineEdit(self)
        self.machine.setFont(self.font)
        self.machine.setSizePolicy(self.size_policy,self.size_policy)
        self.machine.setText(basic[2])
        
        self.tax_value=QLineEdit(self)
        self.tax_value.setFont(self.font)
        self.tax_value.setSizePolicy(self.size_policy,self.size_policy)
        self.tax_value.setText(str(round(float(basic[3].split(sep=',')[0])*100,2)))
        
        update=QPushButton('Update',self)
        update.setFont(self.font)
        update.setSizePolicy(self.size_policy,self.size_policy)
        update.clicked.connect(self.update_basic_values)
        
        layout=QGridLayout()
        layout.addWidget(mach,0,0)
        layout.addWidget(self.machine,0,1)
        layout.addWidget(tax,1,0)
        layout.addWidget(self.tax_value,1,1)
        layout.addWidget(update,2,0)
        self.update_info.setLayout(layout)
        self.update_info.show()
        
    def update_basic_values(self):
        self.update_info.close()
        location=os.path.join(os.path.join(self.base_directory,
                                           'Saved_Invoices'),
                                            '{}'.format(self.current_job))
        e=open(os.path.join(location,'Basic_Info.csv'),'r')
        basic=e.readlines()
        e.close()
        self.flag=False
        #change the information in basic[2] and basic[3] to match the new values
        if basic[2].split(sep='\n')[0]!=self.machine.text():
            self.old=basic[2].split(sep='\n')[0].replace(' ','_')
            self.cust=basic[1].split(sep='\n')[0].replace(' ','_')
            self.file_name=basic[0].split(sep='\n')[0]+'.pdf'
            self.flag=True
            basic[2]=self.machine.text()
            self.machine_text=basic[2]
            self.machine_label.setText('Machine: {}'.format(self.machine_text))
        if float(basic[3].split(sep=',')[0])!=float(self.tax_value.text())/100:
            try:
                tax_code,ok=QInputDialog.getText(self,'Update Tax Code','Tax Code: ',
                                                 QLineEdit.Normal,
                                     basic[3].split(sep=',')[1].split(sep='\n')[0])
            except:
                tax_code,ok=QInputDialog.getText(self,'Update Tax Code','Tax Code: ',
                                                 QLineEdit.Normal,"")
            basic[3]='{},{}'.format(float(self.tax_value.text())/100,tax_code)
            
        self.tax.emit(float(self.tax_value.text())/100)
        
        f=open(os.path.join(location,'Basic_Info.csv'),'w')
        for i in range(len(basic)):
            if '\n' not in basic[i]:
                f.write('{}\n'.format(basic[i]))
            else:
                f.write('{}'.format(basic[i]))
        f.close()
        
    def move_files(self):
        cust=self.cust
        old=self.old
        file_name=self.file_name
        if self.flag:
        #depending on if the machine has been updated, get rid of the previous
        #version of the file and start change it to the new location
            location=os.path.join(os.path.expanduser('~/Desktop'),
                                  'BEI_Invoices')
            old_location_cust_=os.path.join(os.path.join(location,'Customer'),
                                           cust)
            old_location_cust=os.path.join(old_location_cust_,old)
            old_final_cust=os.path.join(old_location_cust,file_name)
            
            old_location_comp_=os.path.join(os.path.join(location,'Company'),
                                           cust)
            old_location_comp=os.path.join(old_location_comp_,old)
            len_old=len(os.listdir(old_location_comp))
            old_final_comp=os.path.join(old_location_comp,file_name)
            
            if len_old==1:
                shutil.rmtree(old_location_comp)
                shutil.rmtree(old_location_cust)
            else:
                os.unlink(old_final_comp)
                os.unlink(old_final_cust)