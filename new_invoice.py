import sys,os
from pathlib import Path
from PyQt5.QtWidgets import (QApplication, QPushButton,QWidget,QGridLayout,
                             QSizePolicy,QComboBox,QLineEdit,QLabel,
                             QCompleter,QMessageBox,QInputDialog)
from PyQt5.QtGui import QFont,QIcon, QImage, QPalette, QBrush

class New_Invoice(QWidget):
    '''Classs used in setting up all the stuff for a newly started invoice
    In charge of:
        1.) Basic Customer Information
        2.) Launching a new table for parts and labor. 
        3.) Automatically saving the new invoice by the file name given 
    '''
    def __init__(self,font_size,base_directory):
        super().__init__()
        self.completed=False
        self.setGeometry(400,400,600,450)
        #global policies
        self.size_policy=QSizePolicy.Expanding
        self.font=QFont()
        self.font.setPointSize(font_size)
        self.setWindowIcon(QIcon('BEI_Logo.png'))
        backimage=QImage('BEI_Logo.png')
        self.setWindowTitle('Burl Equipment Inc. Customer Beta')
        palette=QPalette()
        palette.setBrush(10,QBrush(backimage))
        self.setPalette(palette)
        #get all the customers from currently in the list
        self.customer_=os.path.join(str(Path(base_directory))
             ,'Customer_Information')
        f=open(os.path.join(self.customer_,'Customers.txt'),'r')
        customer_data=f.readlines()
        f.close()
        customer_list=[i.split(sep='\n')[0] for i in customer_data]
        #call the setup function and show it
        self.basic_information(customer_list)
#        self.show()
        
    def basic_information(self,customers_listed):
        '''Entering basic information:
        '''
        #the baisc information to be entered
        self.job_number=QLineEdit(self)
        self.job_number.setFont(self.font)
        self.job_number.setSizePolicy(self.size_policy,self.size_policy)
        
        self.customer_name=QLineEdit(self)
        self.customer_name.setCompleter(QCompleter(customers_listed))
        self.customer_name.setFont(self.font)
        self.customer_name.setSizePolicy(self.size_policy,self.size_policy)
        self.customer_name.editingFinished.connect(self.fill_information)
        self.machine=QComboBox(self)
        self.machine.setFont(self.font)
        self.machine.setSizePolicy(self.size_policy,self.size_policy)
        self.machine.setEditable(True)
        self.tax_line=QLineEdit(self)
        self.tax_line.setSizePolicy(self.size_policy,self.size_policy)
        self.tax_line.setFont(self.font)
        self.tax_line.setText('0.00')
        self.customer_address_line_1=QLineEdit(self)
        self.customer_address_line_1.setFont(self.font)
        self.customer_address_line_1.setSizePolicy(self.size_policy,
                                                   self.size_policy)
        self.customer_address_line_2=QLineEdit(self)
        self.customer_address_line_2.setFont(self.font)
        self.customer_address_line_2.setSizePolicy(self.size_policy,
                                                   self.size_policy)
        
        #labels for information that should be entered
        self.job_number_label=QLabel('Job Number:',self)
        self.job_number_label.setFont(self.font)
        self.job_number_label.setSizePolicy(self.size_policy,self.size_policy)
        self.machine_label=QLabel('Machine:',self)
        self.machine_label.setFont(self.font)
        self.machine_label.setSizePolicy(self.size_policy,self.size_policy)
        self.customer_name_label=QLabel('Customer Name:',self)
        self.customer_name_label.setFont(self.font)
        self.customer_name_label.setSizePolicy(self.size_policy,
                                               self.size_policy)
        self.tax_line_label=QLabel('Tax(As a Percent)',self)
        self.tax_line_label.setFont(self.font)
        self.tax_line_label.setSizePolicy(self.size_policy,self.size_policy)
        self.customer_address_line_1_label=QLabel('Address Line 1:',self)
        self.customer_address_line_1_label.setFont(self.font)
        self.customer_address_line_1_label.setSizePolicy(self.size_policy,
                                                         self.size_policy)
        self.customer_address_line_2_label=QLabel('Address Line 2:',self)
        self.customer_address_line_2_label.setFont(self.font)
        self.customer_address_line_2_label.setSizePolicy(self.size_policy,
                                                         self.size_policy)
        self.customer_address_line_2.returnPressed.connect(self.information_)
        #button to interface with the total spreadsheet
        self.start=QPushButton('OK',self)
        self.start.setFont(self.font)
        self.start.setSizePolicy(self.size_policy,self.size_policy)
        self.start.clicked.connect(self.information_)

        self.cancel=QPushButton('Cancel',self)
        self.cancel.setFont(self.font)
        self.cancel.setSizePolicy(self.size_policy,self.size_policy)
        self.cancel.clicked.connect(self.close)
        
        self.layout=QGridLayout(self)
        self.layout.addWidget(self.job_number_label,0,0)
        self.layout.addWidget(self.job_number,0,1)
        self.layout.addWidget(self.customer_name_label,1,0)
        self.layout.addWidget(self.customer_name,1,1)
        self.layout.addWidget(self.machine_label,2,0)
        self.layout.addWidget(self.machine,2,1)
        self.layout.addWidget(self.tax_line_label,3,0)
        self.layout.addWidget(self.tax_line,3,1)
        self.layout.addWidget(self.customer_address_line_1_label,4,0)
        self.layout.addWidget(self.customer_address_line_1,4,1)
        self.layout.addWidget(self.customer_address_line_2_label,5,0)
        self.layout.addWidget(self.customer_address_line_2,5,1)
        self.layout.addWidget(self.start,6,0)
        self.layout.addWidget(self.cancel,6,1)
        self.show()
        
    def fill_information(self):
        self.machine.clear()
        customer_name=self.customer_name.text()
        customer_name=customer_name.replace(' ','_')
        self.namer=customer_name
        try:
            machines_=os.path.join(os.path.join(self.customer_,'Machines'),
                                   customer_name)
            f=open(machines_+'.txt','r')
            machine_data=f.readlines()
            f.close()
            self.machines=[i.split(sep='\n')[0] for i in machine_data]
            self.machine.addItems(self.machines)
            self.machine.addItem(' ')
            #take care of getting the customer addresses
            addresses_=os.path.join(os.path.join(self.customer_,'Addresses'),
                                    customer_name)
            f=open(addresses_+'.txt','r')
            address=f.readlines()
            f.close()
            lines=[i.split(sep='\n')[0] for i in address]
            self.customer_address_line_1.setText(lines[0])
            self.customer_address_line_2.setText(lines[1])
        except:
            self.machines=[]
            self.new_=QWidget()
            self.new_.setWindowIcon(QIcon('BEI_Logo.png'))
            self.new_.setWindowTitle('New Customer Intake')
            add=QPushButton('Add Customer',self)
            add.setFont(self.font)
            add.setSizePolicy(self.size_policy,self.size_policy)
            add.clicked.connect(self.new_customer)
            clo=QPushButton('Close',self)
            clo.setFont(self.font)
            clo.setSizePolicy(self.size_policy,self.size_policy)
            clo.clicked.connect(self.new_.close)
            self.line_1=QLineEdit(self)
            self.line_1.setFont(self.font)
            self.line_1.setSizePolicy(self.size_policy,self.size_policy)
            self.line_2=QLineEdit(self)
            self.line_2.setFont(self.font)
            self.line_2.setSizePolicy(self.size_policy,self.size_policy)
            #labels for address entry
            line_1_label=QLabel('Address Line 1:',self)
            line_1_label.setFont(self.font)
            line_1_label.setSizePolicy(self.size_policy,self.size_policy)
            line_2_label=QLabel('Address Line 2:',self)
            line_2_label.setFont(self.font)
            line_2_label.setSizePolicy(self.size_policy,self.size_policy)
            
            layout=QGridLayout()
            layout.addWidget(line_1_label,0,0)
            layout.addWidget(self.line_1,0,1)
            layout.addWidget(line_2_label,1,0)
            layout.addWidget(self.line_2,1,1)
            layout.addWidget(add,2,0)
            layout.addWidget(clo,2,1)
            self.new_.setLayout(layout)
            self.new_.setGeometry(400,400,350,100)
            self.new_.show()
            
    def new_customer(self):
        '''Add the new customer name to the customer file
        '''
        #add the customer name to the list
        f=open(os.path.join(self.customer_,'Customers.txt'),'a+')
        f.write(self.customer_name.text()+'\n')
        f.close()
        #add the customer address file 
        p=open(os.path.join(os.path.join(self.customer_,'Addresses'),
                            self.namer+'.txt'),'w')
        p.write(self.line_1.text()+'\n')
        p.write(self.line_2.text())
        p.close()
        #make a dummy text file to use for machine entering later
        h=open(os.path.join(os.path.join(self.customer_,'Machines'),
                            self.namer+'.txt'),'w')
        h.close()
        #set the customer address to represent the entered information
        self.customer_address_line_1.setText(self.line_1.text())
        self.customer_address_line_2.setText(self.line_2.text())
        self.new_.close()
        
    def information_(self):
        '''Take the information in the fields and make it avaiable to the
        rest of the program
        '''
        self.job_num=self.job_number.text()
        self.customer=self.customer_name.text()
        self.machine_=self.machine.currentText()
        self.tax=float(self.tax_line.text())/100
        if self.tax!=0.0:
            self.tax_code,ok=QInputDialog.getText(self,'Tax Code','Tax Code:',
                                                  QLineEdit.Normal,"")
        else:
            self.tax_code=''
        self.line1=self.customer_address_line_1.text()
        self.line2=self.customer_address_line_2.text()
        #check to see if the machine is already in the system, if not
        #proceed to add it to the system
        if str(self.machine.currentText()) not in self.machines:
            buttonReply=QMessageBox.question(self,'Confirm New Machine',
                                    'Do you want to add {}?'
                                    .format(self.machine.currentText())
                                    ,QMessageBox.Yes | QMessageBox.No
                                    ,QMessageBox.No)
            if buttonReply==QMessageBox.Yes:
                h=open(os.path.join(os.path.join(self.customer_,'Machines'),
                            self.namer+'.txt'),'a+')
                h.write(self.machine.currentText()+'\n')
                h.close()
            
        self.close()
        
if __name__=='__main__':
    app=QApplication(sys.argv)
    win=New_Invoice()
    sys.exit(app.exec_())