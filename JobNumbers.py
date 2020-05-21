import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QWidget,QPushButton,QApplication,
                             QMainWindow,QLineEdit,QVBoxLayout,QSystemTrayIcon,
                             QHBoxLayout,QAction,qApp,QProgressBar,
                             QSizePolicy,QLabel,QGridLayout)
from PyQt5.QtCore import QThread,pyqtSignal
from PyQt5.QtGui import QFont
import os
import time
class Job_Numbers(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title='Job Number Creation'
        self.left=300
        self.top=300
        self.width=400
        self.height=375
        self.setWindowIcon(QIcon('loader.png'))
        self.font=QFont()
        self.font.setPointSize(12)
        self.size_policy=QSizePolicy.Expanding
        self.job_number_locate=os.path.join(os.path.join(os.path.expanduser('~\Desktop'),
                                            'BEI_Invoices'),'Job_Numbers')
        self.loca=os.path.join(self.job_number_locate,'Job_Numbers.csv')
        self.initUI()
          
    def initUI(self):
        '''Setting up the GUI'''
        self.setWindowTitle(self.title)
        self.setGeometry(self.left,self.top,self.width,self.height)
        self.tray=QSystemTrayIcon(self)
        self.tray.setIcon(QIcon('loader.png'))
        
        self.statusBar().showMessage('Alan Burl Job Numbers, All Rights Reserved 2018')
        self.menu=self.menuBar()
        ##Addin the pringing to the menu bar
        self.printe=QAction('Print')
        self.printe.setShortcut('CTRL+P')
        self.printe.triggered.connect(self.prints)
        
        self.exit=QAction('Exit')
        self.exit.setShortcut('CTRL+Q')
        self.exit.triggered.connect(self.close)
        
        self.entry1=QAction('Initial Setup')
        self.entry1.setShortcut('CTRL+I')
        self.entry1.triggered.connect(self.initial_numbers)
        
        self.force_close=QAction('Force Close')
        self.force_close.setShortcut('CTRL+X')
        self.force_close.triggered.connect(self.close_sheet)
        
        ##setting up the menu bar
        self.file= self.menu.addMenu('&File')
        self.file.addActions([self.printe,self.exit,
                              self.entry1,self.force_close])

        self.text1=QLineEdit(self)
        self.text1.setFont(self.font)
        self.text1.setSizePolicy(self.size_policy,self.size_policy)
        self.text2=QLineEdit(self)
        self.text2.setFont(self.font)
        self.text2.setSizePolicy(self.size_policy,self.size_policy)
        
        self.label1=QLabel('First Number:',self)
        self.label1.setFont(self.font)
        self.label1.setSizePolicy(self.size_policy,self.size_policy)
        self.label2=QLabel('Second Number:',self)
        self.label2.setFont(self.font)
        self.label2.setSizePolicy(self.size_policy,self.size_policy)

        self.progress=QProgressBar(self)
        self.progress.setSizePolicy(self.size_policy,self.size_policy)
        
        self.pOk=QPushButton('Write Numbers',self)
        self.pOk.setFont(self.font)
        self.pOk.setSizePolicy(self.size_policy,self.size_policy)
        self.pOk.clicked.connect(self.new_numbers)
        
        self.printer=QPushButton('Print',self)
        self.printer.setFont(self.font)
        self.printer.setSizePolicy(self.size_policy,self.size_policy)
        self.printer.clicked.connect(self.prints)
        
        center=QWidget(self)
        layout=QGridLayout(self)
        layout.addWidget(self.label1,0,0)
        layout.addWidget(self.text1,0,1)
        layout.addWidget(self.label2,1,0)
        layout.addWidget(self.text2,1,1)
        layout.addWidget(self.pOk,2,0)
        layout.addWidget(self.printer,2,1)
        layout.addWidget(self.progress,3,0,1,2)
        center.setLayout(layout)
        self.setCentralWidget(center)
        self.show()

    def new_numbers(self):
        self.th=Thread(directory=self.loca,parent=self)
        self.th.ChangeFirstNumber.connect(self.text1.setText)
        self.th.ChangeLastNumber.connect(self.text2.setText)
        self.th.ChangeProgressBar.connect(self.progress.setValue)
        self.th.start()
        
    def initial_numbers(self):
        first_number=(9260)
        
        self.z=open(self.loca,'w')
        number=first_number
        while number<=first_number+46:
            self.z.write(str(number)+5*','+str(number+1)+',\n\n')
            number+=2
        self.z.close()
    def close_sheet(self):
        self.close()
        
    def prints(self):
        os.startfile(self.loca,'print')
        self.close()
        
class Thread(QThread):
    ChangeFirstNumber=pyqtSignal(str)
    ChangeLastNumber=pyqtSignal(str)
    ChangeProgressBar=pyqtSignal(float)
    
    def __init__(self, directory,parent=None):
        '''Setting up the thread'''
        QThread.__init__(self, parent=parent)
        self.isRunning=True
        self.loca=directory
  
    def run(self):
        '''Writing the job numbers and updating the progress bar'''
        r=open(self.loca,'r')
        lines=r.readlines()
        r.close()
        nums=[]
        for line in lines:
            num=line.split(sep=',')
            nums.append(num)
        first_number=int(nums[-2][-2])
        self.t=open(self.loca,'w')
        new_number=first_number+1
        while new_number<=first_number+47:
            self.t.write(str(new_number)+5*','+str(new_number+1)+',\n\n')
            percent_complete=(new_number+2-first_number)/47
            self.ChangeProgressBar.emit(percent_complete*100)
#            self.ChangeLastNumber.emit(str(new_number))
            new_number+=2
            time.sleep(0.005)
        self.t.close()
        self.ChangeLastNumber.emit(str(new_number))
        self.ChangeFirstNumber.emit(str(first_number))
    
    def stop(self):
        '''Stopping the thread'''
        self.isRunning=False
        self.quit()
        self.wait()
                		
if __name__=='__main__':
    app=QApplication(sys.argv)
    ex=App()
    ex.show()
    sys.exit(app.exec_())