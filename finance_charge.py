#prefined imports
import sys,os,shutil
from pathlib import Path
from PyQt5.QtWidgets import (QApplication, QPushButton,QWidget,QGridLayout,
                             QSizePolicy,QComboBox,QLineEdit,QTextEdit,
                             QMessageBox,QInputDialog,QMainWindow,QAction
                             ,QDockWidget,QTableWidgetItem,QVBoxLayout,
                             QTabWidget,QSystemTrayIcon,QHBoxLayout,QTextBrowser,
                             QLabel,QListView,QAbstractItemView,QCheckBox)
from PyQt5.QtGui import (QFont,QIcon, QImage, QPalette, QBrush,
                         QStandardItemModel,QStandardItem)
from PyQt5.QtCore import Qt,QModelIndex

class Finance_Charges(QWidget):
    commenter=False
    def __init__(self,font, size_policy):
        super().__init__()
        self.font=font
        self.size_policy=size_policy
        self.setWindowTitle('Finance Charges Input')
        self.setWindowIcon(QIcon('BEI_Logo.png'))
        self.partial_payment()
        self.show()
        
    def partial_payment(self):
        self.date_=QLineEdit(self)
        self.date_.setFont(self.font)
        self.date_.setSizePolicy(self.size_policy,self.size_policy)
        
        self.amount_=QLineEdit(self)
        self.amount_.setFont(self.font)
        self.amount_.setSizePolicy(self.size_policy,self.size_policy)
        
        self.date_label=QLabel('Date Applied:',self)
        self.date_label.setFont(self.font)
        self.date_label.setSizePolicy(self.size_policy,self.size_policy)
        
        self.amount_label=QLabel('Finance Charge Amount: $',self)
        self.amount_label.setFont(self.font)
        self.amount_label.setSizePolicy(self.size_policy,self.size_policy)
        
        self.add=QPushButton('Process',self)
        self.add.setFont(self.font)
        self.add.setSizePolicy(self.size_policy,self.size_policy)
        self.add.clicked.connect(self.process)
        
        layout=QGridLayout(self)
        layout.addWidget(self.date_label,0,0)
        layout.addWidget(self.date_,0,1)
        layout.addWidget(self.amount_label,1,0)
        layout.addWidget(self.amount_,1,1)
        layout.addWidget(self.add,3,0,1,2)
        
        self.setLayout(layout)
        
    def process(self):
        self.date=self.date_.text()
        try:
            self.amount=float(self.amount_.text())
            self.close()
        except:
            button=QMessageBox.information(self,'No Amount',
                                           'No amount enetered',
                                           QMessageBox.Ok)
            