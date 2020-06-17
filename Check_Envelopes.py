import sys,os,subprocess,shutil
from PyQt5.QtWidgets import (QApplication, QPushButton,QWidget,QGridLayout,
                             QSizePolicy,QLineEdit,QCompleter,QLabel,
                             QInputDialog)
from PyQt5.QtGui import (QFont,QIcon)
from PyQt5.QtGui import QImage, QPalette, QBrush
class Check_Envelopes(QWidget):
    def __init__(self,base_directory):
        super().__init__()
        base_path=os.path.join(base_directory,'Check_Addresses')
        if 'Check_Addresses' not in os.listdir(base_directory):
            os.mkdir(base_path)
        self.base_path=base_path
        self.setGeometry(400,400,600,450)
        self.size_policy=QSizePolicy.Expanding
        self.font=QFont()
        self.font.setPointSize(12)
        self.setWindowIcon(QIcon('BEI_Logo.png'))
        backimage=QImage('BEI_Logo.png')
        palette=QPalette()
        palette.setBrush(10,QBrush(backimage))
        self.setPalette(palette)
        self.setWindowTitle('Check Envelope Printer')
        
        self.file=os.path.join(base_path,'addresss.txt')
        self.names=[]
        self.names2=[]
        try:
            f=open(self.file,'r')
            self.data=f.readlines()
            f.close()
            for i in range(len(self.data)):
                self.names.append(self.data[i].split(sep=',')[0])
                self.names2.append(self.data[i].split(sep=',')[0].replace('_',' '))
        except:
            self.data=[]
            
        text,ok=QInputDialog.getItem(self,'Envelope Size','Size',['Business','Personal'])
        if ok==True:
            self.type=text
            self.geometry()
        else:
            self.close()
            
    def geometry(self):
        check_label=QLabel('Check wrote to:',self)
        check_label.setFont(self.font)
        check_label.setSizePolicy(self.size_policy,self.size_policy)
        
        address1_label=QLabel('Address Line 1:',self)
        address1_label.setFont(self.font)
        address1_label.setSizePolicy(self.size_policy,self.size_policy)
        address1_label.setStyleSheet('color: white;')
        
        address2_label=QLabel('Address Line 2:',self)
        address2_label.setFont(self.font)
        address2_label.setSizePolicy(self.size_policy,self.size_policy)
        address2_label.setStyleSheet('color: white;')
        
        self.customer_name=QLineEdit(self)
        self.customer_name.setCompleter(QCompleter(self.names2))
        self.customer_name.setFont(self.font)
        self.customer_name.setSizePolicy(self.size_policy,self.size_policy)
#        self.customer_name.returnPressed.connect(self.fill_information)  
        self.customer_name.editingFinished.connect(self.fill_information)
        
        self.address_1=QLineEdit(self)
        self.address_1.setFont(self.font)
        self.address_1.setSizePolicy(self.size_policy,self.size_policy)
        self.address_1.setReadOnly(True)
        
        self.address_2=QLineEdit(self)
        self.address_2.setFont(self.font)
        self.address_2.setSizePolicy(self.size_policy,self.size_policy)
        self.address_2.setReadOnly(True)
        
        process=QPushButton('Print',self)
        process.setFont(self.font)
        process.setSizePolicy(self.size_policy,self.size_policy)
        process.clicked.connect(self.printer)
        
        layout=QGridLayout(self)
        layout.addWidget(check_label,1,0)
        layout.addWidget(self.customer_name,1,1)
        layout.addWidget(address1_label,2,0)
        layout.addWidget(self.address_1,2,1)
        layout.addWidget(address2_label,3,0)
        layout.addWidget(self.address_2,3,1)
        layout.addWidget(process,4,0,1,2)
        self.setLayout(layout)
        self.show()
        
    def fill_information(self):
        #get the name
        self.name=self.customer_name.text().replace(' ','_')
        line=0
        if self.name in self.names:
            for i in range(len(self.names)):
                if self.name in self.names[i]:
                    line=i
            self.address_1.setText(self.data[line].split(sep=',')[1].replace('.',','))
            self.address_2.setText(self.data[line].split(sep=',')[2].replace('.',','))
        else:
            self.new_payment()
        
    def new_payment(self):
        self.new_=QWidget()
        self.new_.setWindowIcon(QIcon('BEI_Logo.png'))
        self.new_.setWindowTitle('New Check Intake')
        add=QPushButton('Add Check',self)
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
        self.line1=self.line_1.text().replace(',','.')
        self.line2=self.line_2.text().replace(',','.')
        self.new_.close()
        self.address_1.setText(self.line_1.text())
        self.address_2.setText(self.line_2.text())
        
        f=open(self.file,'a')
        f.write('{},{},{},\n'.format(self.name,self.line1,self.line2))
        f.close()
        
    def printer(self):
        self.generate_latex()
        self.close()
        
    def generate_latex(self):
        replace=['@','#','$','%','&']
        customer=self.customer_name.text()
        address1=self.address_1.text()
        address2=self.address_2.text()
        tex_location=os.path.join(self.base_path,
                                  self.name.replace(' ','_')+'.tex')
        file=open(tex_location,'w')
        header_return=[r'\documentclass{letter}',
                r'\usepackage{graphics}',
                r'\usepackage[envelope]{envlab}'.replace('envelope',
                             self.type.lower()+'envelope'),
                r'\makelabels',r'\begin{document}',
                r'\startlabels',
                r'\mlabel{Burl Equipment Inc\\ PO Box 347\\ Cimarron KS 67835}{']
        
        for i in header_return:
           file.write(i+'\n')
           
        customer1=customer
        for i in replace:
            customer1=customer1.replace(i,r'\{}'.format(i))
            address1=address1.replace(i,r'\{}'.format(i))
            address2=address2.replace(i,r'\{}'.format(i))
            
        file.write(r'{}\\{}\\{}'.format(customer1,address1,address2))
        file.write(r'}')
        file.write(r'\end{document}')
        file.close()
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        subprocess.call(['pdflatex',tex_location],startupinfo=startupinfo)
        os.unlink(os.path.join(os.getcwd(),self.name.replace(' ','_')+'.aux'))
        os.unlink(os.path.join(os.getcwd(),self.name.replace(' ','_')+'.log'))     
        shutil.move(os.path.join(os.getcwd(),self.name.replace(' ','_')+'.pdf'),
                    os.path.join(self.base_path,self.name.replace(' ','_')+'.pdf'))        
        os.unlink(os.path.join(self.base_path,self.name.replace(' ','_')+'.tex'))
        
        self.print_pdf()
    def print_pdf(self):
        loc=os.path.join(self.base_path,self.name.replace(' ','_')+'.pdf')
        os.startfile(loc,'print')
        
if __name__=='__main__':
    app=QApplication(sys.argv)
    a=Check_Envelopes(os.getcwd())
    sys.exit(app.exec_())