import subprocess,psutil
import sys,os,time
import shutil
from pathlib import Path
from PyQt5.QtWidgets import (QApplication, QPushButton,QWidget,QGridLayout,
                             QSizePolicy,QLineEdit,QTextEdit,
                             QMessageBox,QInputDialog,QMainWindow,QAction
                             ,QDockWidget,QTableWidgetItem,QVBoxLayout,
                             QTabWidget,QSystemTrayIcon,QListView,
                             QAbstractItemView,QCompleter,QLabel,QMdiArea,
                             QMdiSubWindow,QStatusBar,QHBoxLayout,QFileDialog)
from PyQt5.QtGui import (QFont,QIcon,QStandardItemModel,QStandardItem)
from PyQt5.QtCore import Qt,QModelIndex

class Envelope_Selector(QWidget):
    def __init__(self,base_directory):
        super().__init__()
        self.base_directory=base_directory
        self.font=QFont()
        self.font.setPointSize(12)
        self.size_policy=QSizePolicy.Expanding
        
    def geometry(self):
        self.print=QPushButton('Print Envelopes',self)
        self.print.setSizePolicy(self.size_policy,self.size_policy)
        self.print.setFont(self.font)
        self.print.clicked.connect(self.print_env)
        
        self.jobs=QListView(self)
        self.jobs.setFont(self.fonts)
        self.jobs.setSizePolicy(self.size_policy,self.size_policy)
        
        model=QStandardItemModel(self.jobs)
        #get the current jobs
        dire=os.path.join(self.base_directory,'Saved_Invoices')
        dirs=os.listdir(dire)
        
        for it in dirs:
            item=QStandardItem(it)
            item.setCheckable(True)
            model.appendRow(item)
    def item(self):
        pass
        
    def print_env(self):
        pass