#prefined imports
import os,sys
from PyQt5.QtWidgets import (QApplication, QPushButton,QWidget,QGridLayout,
                             QSizePolicy,QComboBox,QLineEdit,QTextEdit,
                             QMessageBox,QInputDialog,QMainWindow,QAction
                             ,QDockWidget,QTableWidgetItem,QVBoxLayout,
                             QTabWidget,QSystemTrayIcon,QHBoxLayout,QTextBrowser,
                             QLabel,QListView,QAbstractItemView,QCompleter)
from PyQt5.QtGui import (QFont,QIcon, QImage, QPalette, QBrush,
                         QStandardItemModel,QStandardItem)

class Change_Customer_Name(QWidget):
    def __init__(self,base_directory,current_customer):
        super().__init__()
        self.size_policy=QSizePolicy.Expanding
        self.font=QFont()
        self.font.setPointSize(12)
        
        self.base_directory=base_directory
        self.current_customer=current_customer
        self.setGeometry(400,400,700,200)
        self.setWindowTitle('Change Customer')
        self.setWindowIcon(QIcon('BEI_Logo.png'))
        self.customer_=os.path.join(base_directory,'Customer_Information')       
        f=open(os.path.join(self.customer_,'Customers.txt'),'r')
        customer_data=f.readlines()
        f.close()
        customer_list=[i.split(sep='\n')[0] for i in customer_data]
        #call the setup function and show it
        
        self.geomtery(customer_list)
        self.show()
        
    def geomtery(self,customer_list):
        current_label=QLabel('Current Customer Name:',self)
        current_label.setSizePolicy(self.size_policy,self.size_policy)
        current_label.setFont(self.font)
    
        current_customer=QLineEdit(self)
        current_customer.setSizePolicy(self.size_policy,self.size_policy)
        current_customer.setFont(self.font)
        current_customer.setReadOnly(True)
        current_customer.setText(self.current_customer)
        
        new_customer=QLabel('New Customer:', self)
        new_customer.setSizePolicy(self.size_policy,self.size_policy)
        new_customer.setFont(self.font)
        
        self.new_customer=QLineEdit(self)
        self.new_customer.setSizePolicy(self.size_policy,self.size_policy)
        self.new_customer.setFont(self.font)
        self.new_customer.setCompleter(QCompleter(customer_list))
        
        self.update=QPushButton('Update',self)
        self.update.setSizePolicy(self.size_policy,self.size_policy)
        self.update.setFont(self.font)
        self.update.clicked.connect(self.updater)
        
        layout=QGridLayout()
        layout.addWidget(current_label,0,0)
        layout.addWidget(current_customer,0,1)
        layout.addWidget(new_customer,1,0)
        layout.addWidget(self.new_customer,1,1)
        layout.addWidget(self.update,2,0,1,3)
        self.setLayout(layout)
        
    def updater(self):
        self.close()

if __name__=='__main__':
    base_directory=os.path.join(os.environ['USERPROFILE'],'BEI_Invoices')
    app=QApplication(sys.argv)
    win=Change_Customer_Name(base_directory,'BEI')
    sys.exit(app.exec_())