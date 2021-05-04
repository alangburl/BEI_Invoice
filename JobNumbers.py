import sys
from PyQt5.QtWidgets import (QWidget,QPushButton,QApplication,
                             QMainWindow,QLineEdit,QSystemTrayIcon,
                             QSizePolicy,QLabel,QGridLayout,QInputDialog)
from PyQt5.QtCore import (QIODevice, QFile, Qt, QMarginsF, QRect)
from PyQt5.QtGui import QPdfWriter, QPainter,QFont,QIcon

import os
class Job_Numbers(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title='Job Number Creation'
        self.left=300
        self.top=300
        self.width=400
        self.height=375
        self.setWindowIcon(QIcon('BEI_Logo.png'))
        self.font=QFont()
        self.font.setPointSize(12)
        self.size_policy=QSizePolicy.Expanding
        self.job_number_locate=os.path.join(os.path.join(
            os.path.expanduser('~\Desktop'),
                                            'BEI_Invoices'),'Job_Numbers')
        self.init_file=os.path.join(self.job_number_locate,'InitialNumber.init')
        self.loca=os.path.join(self.job_number_locate,'Job_Numbers.pdf')
        try:
            self.initUI()
        except:
            self.initializer()
            self.initUI()
          
    def initUI(self):
        '''Setting up the GUI'''
        self.setWindowTitle(self.title)
        self.setGeometry(self.left,self.top,self.width,self.height)
        self.tray=QSystemTrayIcon(self)
        self.tray.setIcon(QIcon('loader.png'))
        
        self.text1=QLineEdit(self)
        self.text1.setFont(self.font)
        self.text1.setSizePolicy(self.size_policy,self.size_policy)
        self.text2=QLineEdit(self)
        self.text2.setFont(self.font)
        self.text2.setSizePolicy(self.size_policy,self.size_policy)
        self.text2.setReadOnly(True)
        
        self.label1=QLabel('First Number:',self)
        self.label1.setFont(self.font)
        self.label1.setSizePolicy(self.size_policy,self.size_policy)
        self.label2=QLabel('Last Number:',self)
        self.label2.setFont(self.font)
        self.label2.setSizePolicy(self.size_policy,self.size_policy)
        
        self.pOk=QPushButton('Write Numbers',self)
        self.pOk.setFont(self.font)
        self.pOk.setSizePolicy(self.size_policy,self.size_policy)
        self.pOk.clicked.connect(self.new_numbers)
        
        self.printer=QPushButton('Print',self)
        self.printer.setFont(self.font)
        self.printer.setSizePolicy(self.size_policy,self.size_policy)
        self.printer.clicked.connect(self.prints)
        self.printer.setEnabled(False)
        
        f=open(self.init_file,'r')
        val=f.readline()
        f.close()
        self.text1.setText(val)
        
        center=QWidget(self)
        layout=QGridLayout(self)
        layout.addWidget(self.label1,0,0)
        layout.addWidget(self.text1,0,1)
        layout.addWidget(self.label2,1,0)
        layout.addWidget(self.text2,1,1)
        layout.addWidget(self.pOk,2,0)
        layout.addWidget(self.printer,2,1)
        center.setLayout(layout)
        self.setCentralWidget(center)
        self.show()

    def new_numbers(self):
        self.printer.setEnabled(True)
        self.pOk.setEnabled(False)
        val=self.text1.text()
        a=PDFWriter(val, self.loca)
        top=60
        last=a.write_values(int(val),top)
        self.text2.setText(str(last))
        f=open(self.init_file,'w')
        f.write(str(last+1))
        f.close()
        
    def prints(self):
        self.pOk.setEnabled(True)
        os.startfile(self.loca,'print')
        f=open(self.init_file,'r')
        val=f.readline()
        f.close()
        self.text1.setText(val)
        self.text2.setText('')
        
    def initializer(self):
        val,ok=QInputDialog.getInt(self, 'Initial Number', 'Number',10840,
                                   10840,100000)
        if ok:
            f=open(self.init_file,'w')
            f.write(str(val))
            f.close()
                		
class PDFWriter():
    def __init__(self,first_value,file_name):
        super().__init__()
        self.file=QFile(file_name)
        self.file.open(QIODevice.WriteOnly)
        
        self.writer=QPdfWriter(self.file)
        self.writer.setResolution(300)
        self.writer.setPageMargins(QMarginsF(30,30,30,30))
        
        self.painter=QPainter(self.writer)
        self.painter.setFont(QFont('times',14))
        self.font=QFont()
        self.font.setPointSize(14)
            
    def write_values(self,value,top):
        for i in range(value,value+60):
            line='{}'.format(i)
            if i%2==0:
                location=QRect(0,top,500,60)
                self.painter.drawText(location, Qt.AlignLeft, line)
            elif i%2==1:
                location=QRect(700,top,500,60)
                self.painter.drawText(location, Qt.AlignRight, line)
                top+=110
        self.painter.end()
        self.file.close()
        return value+59
    
if __name__=='__main__':
    app=QApplication(sys.argv)
    ex=Job_Numbers()
    sys.exit(app.exec_())