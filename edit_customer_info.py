#prefined imports
import os
from PyQt5.QtWidgets import (QApplication, QPushButton,QWidget,QGridLayout,
                             QSizePolicy,QComboBox,QLineEdit,QTextEdit,
                             QMessageBox,QInputDialog,QMainWindow,QAction
                             ,QDockWidget,QTableWidgetItem,QVBoxLayout,
                             QTabWidget,QSystemTrayIcon,QHBoxLayout,QTextBrowser,
                             QLabel,QListView,QAbstractItemView)
from PyQt5.QtGui import (QFont,QIcon, QImage, QPalette, QBrush,
                         QStandardItemModel,QStandardItem)
from PyQt5.QtCore import Qt,QModelIndex

class Edit_Customer_Information(QWidget):
    def __init__(self,font,size_policy,base_directory):
        super().__init__()
        self.setWindowIcon(QIcon('BEI_Logo.png'))
        self.setWindowTitle('Update Customer Information')
        self.font=font
        self.size_policy=size_policy
        self.base_directory=base_directory
        self.setup()

    def setup(self):
        '''Setup the cheat sheet viewing
        '''
        self.display=QTextEdit(self)
        self.display.setFont(self.font)
        self.display.setSizePolicy(self.size_policy,self.size_policy)
#        self.display.setReadOnly(True)
        
        self.options=QListView(self)
        self.options.setFont(self.font)
        self.options.setSizePolicy(self.size_policy,self.size_policy)
        self.options.setEditTriggers(QAbstractItemView.NoEditTriggers)
        
        self.save=QPushButton('Update',self)
        self.save.setFont(self.font)
        self.save.setSizePolicy(self.size_policy,self.size_policy)
        self.save.clicked.connect(self.save_info)
        self.save.setEnabled(False)
        
        layout=QGridLayout(self)
        layout.addWidget(self.options,0,0)
        layout.addWidget(self.display,0,1)
        layout.addWidget(self.save,1,0)        
        self.setLayout(layout)
        
        #get the different topics from cheat_sheet_topics.txt
        c=open(os.path.join(os.path.join(self.base_directory,
                                         'Customer_Information'),
                                        'Customers.txt'),'r')
        c_data=c.readlines()
        c.close()
        if len(c_data)==0:
            replay=QMessageBox.information(self,'No Customers',
                        'There are currently no customers',QMessageBox.Ok)
            if replay==QMessageBox.Ok:
                self.close()
        else:
            self.topics=[]
            for i in sorted(c_data):
                self.topics.append(i.replace('\n',''))
        
            self.entry=QStandardItemModel()
            self.options.setModel(self.entry)
            
            self.options.doubleClicked[QModelIndex].connect(self.openFile)
            for tex in self.topics:
                self.entry.appendRow(QStandardItem(tex))
            self.show()
        
    def openFile(self,index):
        self.save.setEnabled(True)
        item=self.entry.itemFromIndex(index)
        text=str(item.text()).replace(' ','_')
        self.customer=text
        #open the text file associated with the clicked item
        cust=os.path.join(self.base_directory,'Customer_Information')
        u=open(os.path.join(os.path.join(cust,'Addresses'),
                            '{}.txt'.format(text)),'r')
        data=u.readlines()
        u.close()
        combi=''
        for i in data:
            combi+=i
        self.display.setText(combi)
    
    def save_info(self):
        cust=os.path.join(self.base_directory,'Customer_Information')
        u=open(os.path.join(os.path.join(cust,'Addresses'),
                            '{}.txt'.format(self.customer)),'w')
        u.write(self.display.toPlainText())
        u.close()
        QMessageBox.information(self,'Saved',
                                '{} information updated'.format(self.customer),
                                QMessageBox.Ok)