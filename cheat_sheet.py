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

class Read_Cheat_Sheet(QWidget):
    def __init__(self,font,size_policy,base_directory):
        super().__init__()
        self.setWindowIcon(QIcon('BEI_Logo.png'))
        self.setWindowTitle('Cheat Sheet Reading')
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
        self.display.setReadOnly(True)
        
        self.options=QListView(self)
        self.options.setFont(self.font)
        self.options.setSizePolicy(self.size_policy,self.size_policy)
#        self.options.setReadOnly(True)
        self.options.setEditTriggers(QAbstractItemView.NoEditTriggers)
        
        layout=QHBoxLayout(self)
        layout.addWidget(self.options)
        layout.addWidget(self.display)
        self.setLayout(layout)
        
        #get the different topics from cheat_sheet_topics.txt
        c=open(os.path.join(os.path.join(self.base_directory,'Cheat_Sheets'),
                            'Topics.txt'),'r')
        c_data=c.readlines()
        c.close()
        if len(c_data)==0:
            replay=QMessageBox.information(self,'No Cheat Sheets',
                        'There are currently no cheat sheets',QMessageBox.Ok)
            if replay==QMessageBox.Ok:
                self.close()
        else:
            self.topics=[]
            for i in c_data:
                self.topics.append(i.replace('\n',''))
        
            self.entry=QStandardItemModel()
            self.options.setModel(self.entry)
            
            self.options.doubleClicked[QModelIndex].connect(self.openFile)
            for tex in self.topics:
                self.entry.appendRow(QStandardItem(tex))
            self.show()
        
    def openFile(self,index):
        item=self.entry.itemFromIndex(index)
        text=str(item.text()).replace(' ','_')
        #open the text file associated with the clicked item
        u=open(os.path.join(os.path.join(self.base_directory,'Cheat_Sheets'),
                            '{}.txt'.format(text)),'r')
        data=u.readlines()
        u.close()
        combi=''
        for i in data:
            combi+=i
        self.display.setText(combi)
        
class Write_Cheat_Sheet(QWidget):
    def __init__(self,font,size_policy,base_directory):
        super().__init__()
        self.setWindowIcon(QIcon('BEI_Logo.png'))
        self.setWindowTitle('Cheat Sheet Update')
        self.font=font
        self.size_policy=size_policy
        self.base_directory=base_directory
        self.cheat_location=os.path.join(base_directory,'Cheat_Sheets')
        self.update_cheat_sheet()   
        self.show()
        
    def update_cheat_sheet(self):
        self.topic=QLineEdit(self)
        self.topic.setFont(self.font)
        self.topic.setSizePolicy(self.size_policy, self.size_policy)
        
        self.prompt=QTextEdit(self)
        self.prompt.setFont(self.font)
        self.prompt.setSizePolicy(self.size_policy,self.size_policy)
        
        self.topic_label=QLabel('Topic',self)
        self.topic_label.setFont(self.font)
        self.topic_label.setSizePolicy(self.size_policy,self.size_policy)
        
        self.prompt_l=QLabel('Text',self)
        self.prompt_l.setFont(self.font)
        self.prompt_l.setSizePolicy(self.size_policy, self.size_policy)
        
        self.save=QPushButton('Save', self)
        self.save.setFont(self.font)
        self.save.setSizePolicy(self.size_policy,self.size_policy)
        self.save.clicked.connect(self.save_data)
        
        layout=QGridLayout(self)
        layout.addWidget(self.topic_label,0,0)
        layout.addWidget(self.topic,1,0)
        layout.addWidget(self.prompt_l,0,1)
        layout.addWidget(self.prompt,1,1,1,4)
        layout.addWidget(self.save,2,0)
        self.setLayout(layout)
        
    def save_data(self):
        #check to see if the topic already exists
        a=open(os.path.join(self.cheat_location,'Topics.txt'),'r')
        t_data=a.readlines()
        a.close()
        filler=[]
        for i in t_data:
            filler.append(i.replace('\n',''))
        if self.topic.text() not in filler:
            #append to the topics file
            h=open(os.path.join(self.cheat_location,'Topics.txt'),'a+')
            h.write('{}\n'.format(self.topic.text()))
            h.close()
            
        #create the prompt file and write it
        tex=self.topic.text().replace(' ','_')
        t=open(os.path.join(self.cheat_location,'{}.txt'.format(tex)),'w')
        t.write(self.prompt.toPlainText())
        t.close()
        self.close()
    