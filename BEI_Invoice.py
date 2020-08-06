#imports from other scripts for the purpose of spliting the file size up
from new_invoice import New_Invoice
from parts_tabs import Parts_Tabs
from labor_tabs import Labor_Tabs
from table_widget import Table
from labor_rates import Labor_Rates
from JobNumbers import Job_Numbers
from cheat_sheet import Read_Cheat_Sheet, Write_Cheat_Sheet
from partial_payment import Partial_Payments
from finance_charge import Finance_Charges
import PDF_Builder_2 as pdf2
import first_initialization as initi
from save_threader import Saver
from edit_customer_info import Edit_Customer_Information as EDI
from enevelope_writer import Enevelope_Writer as EWriter
from Envelope_printer import Envelope_Printer as EP
from Check_Envelopes import Check_Envelopes as CE
import Version_Control as VC
from Change_Customer import Change_Customer as CC
#prefined imports
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
                             QMdiSubWindow,QStatusBar,QHBoxLayout,QMenu)
from PyQt5.QtGui import (QFont,QIcon,QStandardItemModel,QStandardItem)
from PyQt5.QtCore import Qt,QModelIndex
class Invoice(QMainWindow):
    '''Runs the main window of the invoice development
    Calls the table to be used for parts and labor from
    table_widget.py
    '''
    invoice_count=0
    total_parts_=0
    labor_supplies_=0
    recent_open=False
    start_flag=False
    current_job=str
    labor_=0
    parts_=0
    supplies=0
    freight_=0
    subtotal=0
    taxed=0
    totals=0
    tax=0
    partial=0
    finance=0
    new_total=0
    open_list=[]
    printed_list={}
    def __init__(self):
        '''Initialize the window and get pertinent information read in:
            Set the window size
            Set the picture to be a BEI logo
            Read in the standard labor rates
            '''
        super().__init__()
        self.size_policy=QSizePolicy.Expanding
        self.font=QFont()
        self.font.setPointSize(12)
        self.showMaximized()
        self.setWindowIcon(QIcon('BEI_Logo.png'))
#        backimage=QImage('BEI_Logo.png')
        self.setWindowTitle('Burl Equipment Inc. Invoices Beta')
        self.tray=QSystemTrayIcon(self)
        self.tray.setIcon(QIcon('BEI_Logo.png'))
        self.base_directory=str(Path(
                os.path.join(os.environ['USERPROFILE'],'BEI_Invoices')))
        
        self.show()
        self.menu_bar()
        self.statusbar=QStatusBar()
        self.setStatusBar(self.statusbar)
        #this is the first time start up section, should only run the very 
        #first time
        base_entries=os.listdir(os.environ['USERPROFILE'])
        if 'BEI_Invoices' not in base_entries:
            initi.First_Run(self.base_directory)
             
    def menu_bar(self):
        '''Create the menu bar for the main window will include
                Name:       Shortcut:         Function called:
            File:
                New         CTRL+N            new_invoice_begin
                Open        CTRL+O            existing_invoice_open
                Save        CTRL+S              print_invoice
                Quit        ALT       save_invoice
                Print       CTRL+P   +F4            exit_system
            Edit:
                Change Labor Rates            labor_rates
            View:
                View Totals                   view_totals
                View Labor Breakdown          labor_breakdown
            Help:
                View Current Cheat Sheet      cheat_sheet
                Add New Task to Cheat Sheet   add_cheat_task
        '''        
        self.menuFile = self.menuBar().addMenu("&File")
        self.actionNew=QAction('&New',self)
        self.actionNew.setShortcut('Ctrl+N')
        self.actionNew.triggered.connect(self.new_invoice_begin)        
        self.actionOpen = QAction("&Open", self)
        self.actionOpen.setShortcut('Ctrl+O')
        self.actionOpen.triggered.connect(self.existing_invoice_open)
        self.actionSave=QAction('&Save',self)
        self.actionSave.setShortcut('Ctrl+S')
        self.actionSave.setDisabled(True)
        self.actionSave.triggered.connect(self.save_invoice)
#        self.actionImport=QAction('&Import Old Job',self)
#        self.actionImport.triggered.connect(self.old_job)
#        self.actionImport.setShortcut('Ctrl+I')
        self.printMainMenu=QMenu('Print',self)
        
        self.actionPrint=QAction('&Print All',self)
        self.actionPrint.setShortcut('Ctrl+P')
        self.actionPrint.setDisabled(True)
        self.actionPrint.triggered.connect(self.print_invoice)
        
        self.actionPrintCust=QAction('&Print Customer',self)
        self.actionPrintCust.setDisabled(True)
        self.actionPrintCust.triggered.connect(self.print_customer)
        
        self.actionPrintCom=QAction('&Print Company',self)
        self.actionPrintCom.setDisabled(True)
        self.actionPrintCom.triggered.connect(self.print_company)
        self.printMainMenu.addActions([self.actionPrint,self.actionPrintCom,
                                      self.actionPrintCust])
        
        self.printMenu=QMenu('Print Envelopes',self)
        self.actionEnvelope=QAction('&Print All Billed Customer Envelopes',self)
        self.actionEnvelope.triggered.connect(self.envelop_write)
        self.actionEnvelope.setShortcut('Ctrl+E')
        self.actionEnvelope.setDisabled(True)

        self.actionEnvelope1=QAction('&Print Single Billed Customer Envelope',self)
        self.actionEnvelope1.triggered.connect(self.envelop_write1)
        self.actionEnvelope1.setShortcut('Ctrl+R')
        
        self.actionBilledEnvelopes=QAction('&Print Check Envelope',self)
        self.actionBilledEnvelopes.triggered.connect(self.billing_envelopes)
        self.actionBilledEnvelopes.setShortcut('Ctrl+C')
        
        self.printMenu.addActions([self.actionEnvelope,self.actionEnvelope1,
                                   self.actionBilledEnvelopes])
        
        self.actionQuit=QAction('&Exit',self)
        self.actionQuit.triggered.connect(self.closing)
        self.actionQuit.setShortcut('Alt+F4')
        self.menuFile.addActions([self.actionNew, self.actionOpen,
                                  self.actionSave])
        self.menuFile.addMenu(self.printMainMenu)
        self.menuFile.addMenu(self.printMenu)
        self.menuFile.addAction(self.actionQuit)
        
        self.menuEdit=self.menuBar().addMenu('&Edit')
        self.menuEdit_Change_In=QMenu('Change Basic Invoice Information',self)
        self.menuEdit_Change_Sy=QMenu('Change Operating Data',self)
        
        self.actionLaborRates=QAction('&Change Standard Labor Rates',self)
        self.actionLaborRates.triggered.connect(self.labor_rates)
        self.actionAddTechnician=QAction('&Add Technician',self)
        self.actionAddTechnician.triggered.connect(self.add_tech)
        self.actionChangeDate=QAction('&Change Invoice Date',self)
        self.actionChangeDate.triggered.connect(self.date_change)
        self.actionChangeCustomerAddress=QAction('&Change Customer Address',self)
        self.actionChangeCustomerAddress.triggered.connect(self.change_address)
        
        self.actionBasicInfo=QAction('&Change Basic Information',self)
        self.actionBasicInfo.triggered.connect(self.change_basic_info)
        self.actionChangeCustomer=QAction('&Change Customer Name',self)
        self.actionChangeCustomer.triggered.connect(self.change_customer)
        self.actionChangeCustomer.setDisabled(True)
        self.actionBasicInfo.setDisabled(True)
        self.menuEdit_Change_In.addActions([self.actionBasicInfo,
                                            self.actionChangeCustomer])
    
        self.menuEdit_Change_Sy.addActions([self.actionLaborRates,
                                            self.actionAddTechnician,
                                            self.actionChangeDate,
                                            self.actionChangeCustomerAddress])
        self.menuEdit.addMenu(self.menuEdit_Change_In)
        self.menuEdit.addMenu(self.menuEdit_Change_Sy)
        
        self.menuView=self.menuBar().addMenu('&View')
        self.actionViewLaborBreakdown=QAction('&View Labor Breakdown',self)
        self.actionViewLaborBreakdown.setDisabled(True)
        self.actionViewLaborBreakdown.triggered.connect(self.breakdown)
        self.actionViewAllWindows=QAction('&View All Windows',self)
        self.actionViewAllWindows.setDisabled(True)
        self.actionViewAllWindows.triggered.connect(self.view_windows)
        self.actionViewCutomer=QAction('&View Customer Invoice',self)    
        self.actionViewCutomer.triggered.connect(self.view_customer)
        self.actionViewCutomer=QAction('&View Customer Invoice',self)    
        self.actionViewCutomer.triggered.connect(self.view_customer)
        self.actionViewCutomer.setEnabled(False)
        self.actionViewCompany=QAction('&View Company Invoice',self)    
        self.actionViewCompany.triggered.connect(self.view_company)
        self.actionViewCompany.setEnabled(False)
        self.menuView.addActions([self.actionViewLaborBreakdown,
                                  self.actionViewAllWindows,
                                  self.actionViewCutomer,
                                  self.actionViewCompany])
    
        self.actionJobNumbers=QAction('&More Job Numbers',self)
        self.actionJobNumbers.triggered.connect(self.new_job_nums)
        self.menuJobNumbers=self.menuBar().addMenu('Job Numbers')
        self.menuJobNumbers.addAction(self.actionJobNumbers)
    
        self.menuPayment=self.menuBar().addMenu('&Finance/Payments')
        self.actionPartialPayment=QAction('&Partial Payment',self)
        self.actionPartialPayment.triggered.connect(self.partial_payment)
        self.actionPartialPayment.setDisabled(True)
        self.actionFinanceCharges=QAction('&Add Finance Charges',self)
        self.actionFinanceCharges.triggered.connect(self.finance_charges)
        self.actionFinanceCharges.setDisabled(True)
        self.menuPayment.addActions([self.actionPartialPayment,
                                     self.actionFinanceCharges])
        
        self.menuHelp=self.menuBar().addMenu('&Help')
        self.actionViewCheatSheet=QAction('&View Cheat Sheet',self)
        self.actionViewCheatSheet.triggered.connect(self.cheat_sheet)
        self.actionNewCheat=QAction('&Add New Item to Cheat Sheet',self)
        self.actionNewCheat.triggered.connect(self.add_cheat_task)
        self.actionUpdate=QAction('&Update Application')
        self.actionUpdate.triggered.connect(self.updater)
        self.menuHelp.addActions([self.actionViewCheatSheet,
                                  self.actionNewCheat,self.actionUpdate])   
    def new_invoice_begin(self):
        '''Entering basic information:
            Job Number:
            Machine:
            Customer Name:
        '''
        try:
            self.docked.close()
            self.docked2.close()
            self.totals_table.close()
            self.save_invoice()
            self.new_window=New_Invoice(12,self.base_directory)
#            self.new_window.basic_information()
            self.new_window.start.clicked.connect(self.job_num_insertion)
            self.new_window.customer_address_line_2.returnPressed.connect(self.new_window.information_)
            self.new_window.customer_address_line_2.returnPressed.connect(self.job_num_insertion)
        except:
            self.new_window=New_Invoice(12,self.base_directory)
#            self.new_window.basic_information()
            self.new_window.start.clicked.connect(self.job_num_insertion)
            self.new_window.customer_address_line_2.returnPressed.connect(self.new_window.information_)
            self.new_window.customer_address_line_2.returnPressed.connect(self.job_num_insertion)
            
            
    def job_num_insertion(self):
        '''Call the table with the job number given in the new invoice
        '''
        self.reset_data()
        if not self.recent_open:
            self.recent_invoices()
        self.tax=self.new_window.tax
        self.customer=self.new_window.customer.replace('#','')
        self.machine_text=self.new_window.machine_
        self.current_job=self.new_window.job_num
        if self.current_job not in self.open_list:
            self.open_list.append(self.current_job)
            self.recently_opened_invoice.appendRow(QStandardItem(str(self.current_job)))
        self.invoice_count+=1
        #make the folder for this invoice to be saved in
        self.job_dire=os.path.join(os.path.join(self.base_directory,
                                                'Saved_Invoices'),
                                                self.current_job)
        try:
            os.mkdir(self.job_dire)
                    #save the basic information
            location=os.path.join(os.path.join(self.base_directory,
                                       'Saved_Invoices'),self.current_job)
            self.table(self.new_window.job_num)
            basic=os.path.join(location,'Basic_Info.csv')
            f=open(basic,'w')
            f.write(str(self.current_job)+'\n')
    
            f.write(self.new_window.customer+'\n')
            f.write(self.new_window.machine_+'\n')
            f.write('{},{}\n'.format(str(self.new_window.tax),
                    self.new_window.tax_code))
            f.write(self.new_window.line1+'\n')
            f.write(self.new_window.line2+'\n')
            f.close()
        except:
            buttonReply=QMessageBox.question(self,'Confirm New Machine',
                                    'Job Number {} already exist.\nDo you want to overwrite it?'
                                    .format(self.new_window.job_num)
                                    ,QMessageBox.Yes | QMessageBox.No
                                    ,QMessageBox.No)
            if buttonReply==QMessageBox.Yes:
                self.table(self.new_window.job_num)
                location=os.path.join(os.path.join(self.base_directory,
                                           'Saved_Invoices'),self.current_job)
                basic=os.path.join(location,'Basic_Info.csv')
                f=open(basic,'w')
                f.write(str(self.current_job)+'\n')
        
                f.write(self.new_window.customer+'\n')
                f.write(self.new_window.machine_+'\n')
                f.write('{},{}\n'.format(str(self.new_window.tax),
                        self.new_window.tax_code))
                f.write(self.new_window.line1+'\n')
                f.write(self.new_window.line2+'\n')
                f.close()
            elif buttonReply==QMessageBox.No:
                self.current_job=str(self.current_job)
                self.read_in_data()

    def existing_invoice_open(self):
        '''Open an existing invoice
        '''
        try:
            self.docked.close()
            self.docked2.close()
            self.save_invoice()
        except:
            True
        if not self.recent_open:
            self.recent_invoices()
        #get the saved invoices
        loc=os.path.join(self.base_directory,'Saved_Invoices')
        saved_jobs=os.listdir(loc)
        self.existing=QWidget()
        self.existing.setWindowIcon(QIcon('BEI_Logo.png'))
        self.existing.setWindowTitle('Open Existing Invoice')
        self.open=QPushButton('Open',self)
        self.open.setFont(self.font)
        self.open.setSizePolicy(self.size_policy,self.size_policy)
        self.open.clicked.connect(self.reader)
        
        self.job_to_open=QLineEdit(self)
        self.job_to_open.setFont(self.font)
        self.job_to_open.setSizePolicy(self.size_policy,self.size_policy)
        self.job_to_open.setCompleter(QCompleter(saved_jobs))
#        self.job_to_open.returnPressed.connect(self.reader)
        
        layout=QVBoxLayout()
        layout.addWidget(self.job_to_open)
        layout.addWidget(self.open)
        self.existing.setLayout(layout)
        self.existing.setGeometry(400,400,300,100)
        self.existing.show()
        
    def reader(self):
        self.current_job=self.job_to_open.text()
        self.read_in_data()
        self.existing.close()
        
    def table(self,num):
        '''Setup the table for use with a new invoice
        '''
        self.start_flag=True
        self.actionPrint.setEnabled(True)
        self.actionPrintCust.setEnabled(True)
        self.actionPrintCom.setEnabled(True)
        
        self.actionSave.setEnabled(True)
        self.actionViewLaborBreakdown.setEnabled(True)
        self.actionBasicInfo.setEnabled(True)
        self.actionViewAllWindows.setEnabled(True)
        self.actionViewCutomer.setEnabled(True)
        self.actionViewCompany.setEnabled(True)
        self.actionChangeCustomer.setEnabled(True)
        
        self.docked=QMdiSubWindow()
        self.docked.setWindowTitle('Invoice {}'.format(num))
        self.num=num
        self.tabs=QTabWidget(self)
        self.parts=Parts_Tabs(num)
        self.tabs.addTab(self.parts,'Parts')
        self.labor=Labor_Tabs(num)
        self.tabs.addTab(self.labor,'Labor')
        self.docked.setWidget(self.tabs)
        
        self.parts.total.connect(self.calculate_totals)
        self.labor.labor_total.connect(self.calculate_totals)
        
        cust_display=QWidget(self)
        self.cust_label=QLabel('Customer: {}'.format(self.customer),self)
        self.cust_label.setFont(self.font)
        self.machine_label=QLabel('Machine: {}'.format(self.machine_text),self)
        self.machine_label.setFont(self.font)
        lay=QHBoxLayout()
        lay.addWidget(self.cust_label)
        lay.addWidget(self.machine_label)
        cust_display.setLayout(lay)
        
        #design and insert the totals table
        self.totals_table=Table(7,2)
        self.totals_table.tableWidget.setItem(0,0,
                                              QTableWidgetItem('Parts:'))
        self.totals_table.tableWidget.setItem(1,0,
                                              QTableWidgetItem('Labor:'))
        self.totals_table.tableWidget.setItem(2,0,
                                              QTableWidgetItem('Supplies:'))
        self.totals_table.tableWidget.setItem(3,0,
                                              QTableWidgetItem('Freight:'))
        self.totals_table.tableWidget.setItem(4,0,
                                              QTableWidgetItem('Subtotal:'))
        self.totals_table.tableWidget.setItem(5,0,
                                              QTableWidgetItem('Tax: {:.2f}%'
                                               .format(self.tax*100)))
        self.totals_table.tableWidget.setItem(6,0,
                                              QTableWidgetItem('Total:'))
        #set up the comments section
        self.comments=QTextEdit(self)
        self.comments.setFont(self.font)
        self.comments.setSizePolicy(self.size_policy,self.size_policy)
        self.comments.setText('Comments:\n')
        
        self.additional_docking=QWidget(self)
        layout=QVBoxLayout(self)
        layout.addWidget(cust_display)
        layout.addWidget(self.totals_table)
        layout.addWidget(self.comments)
        self.additional_docking.setLayout(layout)
        
        self.docked2=QMdiSubWindow()
        self.docked2.setWidget(self.additional_docking)
        self.docked2.setWindowTitle('Information')
        
        self.mdi=QMdiArea()
        self.mdi.addSubWindow(self.docked2)
        self.mdi.addSubWindow(self.docked)

        self.mdi.tileSubWindows()
        self.setCentralWidget(self.mdi)
#        self.window_saved=self.saveState(1)
        
    def recent_invoices(self):
        '''Show a list of recently opened invoices
        '''
        self.recent_open=True
        self.recent=QDockWidget('Recently opened invoices',self)
        
        self.recently_opened_invoice=QStandardItemModel()
        self.invoices_open=QListView(self)
        self.invoices_open.setFont(self.font)
        self.invoices_open.setSizePolicy(self.size_policy,self.size_policy)
        self.invoices_open.setModel(self.recently_opened_invoice)
        self.invoices_open.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.invoices_open.doubleClicked[QModelIndex].connect(self.recall)
        
        self.notes=QTextEdit(self)
        self.notes.setFont(self.font)
        self.notes.setSizePolicy(self.size_policy,self.size_policy)
        self.notes.setText('Notes:\n')
        
        self.running_info=QWidget(self)
        layout=QVBoxLayout(self)
        layout.addWidget(self.invoices_open)
        layout.addWidget(self.notes)
        self.running_info.setLayout(layout)
        self.recent.setWidget(self.running_info)
        self.addDockWidget(Qt.LeftDockWidgetArea,self.recent)
        
    def recall(self,index):
        item=self.recently_opened_invoice.itemFromIndex(index)
        job_number=item.text()
        self.docked.close()
        self.docked2.close()
        self.save_invoice()
        self.current_job=job_number
        self.read_in_data()
        
    def save_invoice(self,printing=False,no_build=False):
        '''Save both the parts and labor tables
        '''
        if self.current_job==str:
            pass
        else:
            location=os.path.join(os.path.join(self.base_directory,
                                       'Saved_Invoices'),self.current_job)
            parts_file=os.path.join(location,'Parts.csv')
            #first read and write the parts information
            f=open(parts_file,'w')
            row=[]
            for i in range(100):
                try:
                    for j in range(8):
                        if j==0:
                            if self.parts.parts_table.tableWidget.item(i,j).text()!='*':
                                val=float(self.parts.parts_table.tableWidget.item(i,
                                                                          j).text())
                            elif self.parts.parts_table.tableWidget.item(i,j).text()=='*':
                                val=self.parts.parts_table.tableWidget.item(i,j).text()
                            row.append(val)
                        else:
                            try:
                                val=self.parts.parts_table.tableWidget.item(i,
                                                                        j).text()
                                row.append(val)
                            except:
                                row.append('')
                    if '\n' in row[-1]:
                        row[-1]=row[-1].split(sep='\n')[0]
                    row[2]=row[2].replace(',','.')
                    f.write('{},{},{},{},{},{},{},{}\n'.format(*row))
                    row=[]
                except:
                    break
            f.close()
            #save the total table
            total_location=os.path.join(location,'Totals.csv')
            h=open(total_location,'w')
            t_row=[self.parts_,self.labor_,self.supplies,self.freight_,
                   self.subtotal,self.taxed,self.totals]
            for i in t_row:
                try:
                    float(i)
                    h.write('{:.2f}\n'.format(i))
                except:
                    h.write('0')
            h.close()
            #save the comments
            comments_location=os.path.join(location,'Comments.csv')
            v=open(comments_location,'w')
            v.write(self.comments.toPlainText())
            v.close()
            #finally save the labor information
            #get the number of techs showing
            count=self.labor.counts
            
            for l in range(count):
                labor_location=os.path.join(location,'tech{}.csv'.format(l))
                o=open(labor_location,'w')
                #get the data from the labor class
                tech_labor=self.labor.read_data_out(l)
                for k in range(len(tech_labor)):
                    if '\n' in list(tech_labor[k][-1]):
                        tech_labor[k][-1]=float(tech_labor[k][-1])
                    o.write('{},{},{},{},{},{},{},{}\n'.format(*tech_labor[k]))
                o.close()
                
        self.statusbar.showMessage('Invoice {} saved'.format(self.current_job),
                           5000)  
        if no_build==False:
            envelop_writer=EWriter(self.base_directory,self.current_job)
            envelop_writer.generate_latex()
            
            acrobat='Acrobat.exe' in (p.name() for p in psutil.process_iter())
            reader='AcroRd32.exe' in (p.name() for p in psutil.process_iter())
            if acrobat:
                lis=['taskkill','/F','/IM','Acrobat.exe','/T']
                subprocess.call(lis)
            if reader:
                os.system('taskkill /F /IM "AcroRd32.exe" /T')
            
            if printing==False:
                comp_cust=Saver(self,self.base_directory,self.current_job)
                comp_cust.out.connect(self.failure)
                comp_cust.start()
        
    def failure(self,value):
        if value==1:
            QMessageBox.information(self,'Save Failure',
                                        'Closing PDF and trying again',
                                        QMessageBox.Ok)
#            self.save_invoice()
        
    def add_tech(self):
        '''Adding a technician to the company:
            Changes to make:
                Add to the tabs 
                Add standard labor rates
                Change stuff in the base invoice, 
                not sure how this is going to work yet
        '''
        text, okPressed = QInputDialog.getText(self, "Tech Name",
                                               "Tech name:", 
                                               QLineEdit.Normal, "")
        if okPressed and text != '':
            regular, okPressed1 = QInputDialog.getDouble(self, "Regular Rate",
                                                  "Regular Hourly Rate: $",
                                                  80,0,150,2)
            if okPressed1:
                overtime,okPressed2=QInputDialog.getDouble(self,"Overtime Rate",
                                                  "Overtime Hourly Rate: $",
                                                  80,0,150,2)
                if okPressed2:
                    directory=str(Path(os.path.join(os.path.join(os.environ['USERPROFILE']
                    ,'BEI_Invoices')),'Basic_Information_Totals'))
                    tech_data=open(str(Path(os.path.join(directory,'Labor_Rates.csv')))
                    ,'a')
                    tech_data.write('{},{},{}\n'.format(text,regular,overtime))
                    tech_data.close()
                    QMessageBox.information(self,'Updated',
                                            'Application must be restarted to apply these changes',
                                            QMessageBox.Ok)
        
    
    def read_in_data(self):
        self.actionPartialPayment.setEnabled(True)
        self.actionFinanceCharges.setEnabled(True)
        self.invoice_count+=1
        
        if self.current_job not in self.open_list:
            self.open_list.append(self.current_job)
            self.recently_opened_invoice.appendRow(
                    QStandardItem(self.current_job))
        #open the basic information and read the tax percentage
        location=os.path.join(os.path.join(self.base_directory,
                                           'Saved_Invoices'),
                                            '{}'.format(self.current_job))
        e=open(os.path.join(location,'Basic_Info.csv'),'r')
        basic=e.readlines()
        e.close()
        self.customer,self.machine_text=basic[1].replace('\n',''),basic[2].replace('\n','')

        self.tax=float(basic[3].split(sep=',')[0])
        self.table(self.current_job)
        self.machine_label.setText('Machine: {}'.format(self.machine_text))
        self.cust_label.setText('Customer: {}'.format(self.customer))
        #read in the parts data from the file and hand it off the the parts_tab
        #class to be placed in the table
        location=os.path.join(os.path.join(self.base_directory,
                                           'Saved_Invoices'),
                                            '{}'.format(self.current_job))
        parts_location=os.path.join(location,'Parts.csv')
        p_d=open(parts_location,'r')
        p_data=p_d.readlines()
        p_d.close()
        parts_data=[p_data[i].split(sep=',') for i in range(len(p_data))]
        self.parts.read_in_data(parts_data)
        
        #read in the totals information
        totals_information=os.path.join(location,'Totals.csv')
        t_d=open(totals_information,'r')
        t_data=t_d.readlines()
        t_d.close()
        totals=[float(i) for i in t_data]
        #reset all the s
        self.reset_data()
        #try to read in payments and finance cahrges if they exist
        try:
            par_d=open(os.path.join(location,'Payments.csv'),'r')
            self.partial=float(par_d.readlines()[0])
            par_d.close()
        except:
            self.partial=0
        try:
            fin_d=open(os.path.join(location,'Finance.csv'),'r')
            self.finance=float(fin_d.readlines()[0])
            fin_d.close()
        except:
            self.finance=0
        
        self.parts_,self.labor_,self.supplies,self.freight_,self.subtotal,self.taxed,self.totals=totals
        #set the values into the totals table
#        self.totals=self.totals+self.finance-self.partial
        for i in range(len(totals)):
            self.totals_table.tableWidget.setItem(i,1,
                              QTableWidgetItem('${:,.2f}'.format(totals[i])))
        
        #read and put the comments in place
        comments_location=os.path.join(location,'Comments.csv')
        c_data=open(comments_location,'r')
        com_data=c_data.readlines()
        c_data.close()
        combi=''
        for i in com_data:
            combi+=str(i)
        self.comments.setText(combi)
        
        #read in the labor data
        #determine the number of tech there are
        tech_num=0
        dir_=os.listdir(location)
        for i in range(len(dir_)):
            if 'tech' in dir_[i]:
                tech_num+=1
        
        for l in range(tech_num):
            loca=os.path.join(location,'tech{}.csv'.format(l))
            l_data=open(loca,'r')
            lab_data=l_data.readlines()
            l_data.close()
            labor_data=[o.split(sep=',') for o in lab_data]
            self.labor.read_in_data(l,labor_data)
            
    def reset_data(self):
        self.parts_,self.labor_,self.supplies,self.freight_,self.subtotal,self.taxed,self.totals=[0,0,0,0,0,0,0]
        self.partial,self.finance=0,0
            
    def labor_rates(self):
        '''Change the labor rates
        '''
        self.changes=Labor_Rates(self.base_directory,self.font,self.size_policy)
        self.changes.show()
    
    def update_parts_total(self):
        self.parts_calculator()
#        self.parts_=round(self.parts.parts_total,2)
#        self.freight_=round(self.parts.freight_total,2)
        self.totals_table.tableWidget.setItem(0,1,
          QTableWidgetItem('${:,.2f}'.format(self.parts_)))
        self.totals_table.tableWidget.setItem(3,1,
          QTableWidgetItem('${:,.2f}'.format(self.freight_)))
        self.total_parts_=self.parts_+self.freight_
        
    def parts_calculator(self):
        self.parts_=0
        self.freight_=0
#        self.parts.parts_sumation()
#        self.parts_=self.parts.parts_total
#        self.freight_=self.parts.freight_total+1
        
        for i in range(100):
            try:
                self.parts_+=float(self.parts.parts_table.tableWidget.item(i,5).text())
                try:
                    self.freight_+=float(self.parts.parts_table.tableWidget.item(i,6).text())
                except:
                    self.freight_+=0
            except:
                True
        
    def update_labor(self):
        total_labor=0
        for i in range(self.labor.counts):
            total_labor+=self.labor.find_tech_total(i)
        self.totals_table.tableWidget.setItem(1,1,
          QTableWidgetItem('${:,.2f}'.format(round(total_labor,2))))        
        self.totals_table.tableWidget.setItem(2,1,
          QTableWidgetItem('${:,.2f}'.format(round(total_labor*0.05,2))))
        self.supplies=round(total_labor*0.05,2)
        self.labor_=total_labor
        self.labor_supplies_=round(self.labor_,2)+self.supplies
    
    def calculate_totals(self):
        '''Calculate the totals for the totals table and display it
        '''
        self.update_labor()
#        self.parts.parts_sumation()
        self.update_parts_total()
        self.subtotal=self.labor_supplies_+self.total_parts_
        self.totals_table.tableWidget.setItem(
                4,1,QTableWidgetItem('${:,.2f}'.format(self.subtotal)))
        self.taxed=self.tax*self.subtotal
        self.totals_table.tableWidget.setItem(
                5,1,QTableWidgetItem('${:,.2f}'.format(self.taxed)))
        self.totals=self.subtotal+self.taxed+self.finance-self.partial
        self.totals_table.tableWidget.setItem(
                6,1,QTableWidgetItem('${:,.2f}'.format(
                        self.totals)))  
        
    def print_invoice(self):
        '''
        Print the customer and company invoices
        '''
        #make sure the invoice is saved
        self.save_invoice(printing=True)
        self.printed_list[self.current_job]=[self.customer,self.machine_text]
        try:
            pdf2.PDF_Builder(self.current_job,
                                self.base_directory,'Company').print_tex()
            pdf2.PDF_Builder(self.current_job,
                                 self.base_directory,'Customer').print_tex()
        except:
            QMessageBox.information(self,'Print Failure',
                                    'Close file and try again',QMessageBox.Ok)
            
        #first check and see if the Envelopes directory has this 
        #months print list
        envelope_date=EP(self.base_directory,self.customer,self.current_job)
        self.envelope_date=envelope_date.dater()
        self.actionEnvelope.setEnabled(True)
        self.actionEnvelope1.setEnabled(True)
        
    def print_customer(self):
        self.save_invoice(printing=True)
        pdf2.PDF_Builder(self.current_job,
                             self.base_directory,'Customer').print_tex()
    
    def print_company(self):
        self.save_invoice(printing=True)
        pdf2.PDF_Builder(self.current_job,
                                 self.base_directory,'Company').print_tex()
    
    def closing(self):
#        self.save_invoice()
        self.close()
        
    def breakdown(self):
        '''view the labor break down
        '''
        #open the labor rates to get the names 
        loc=os.path.join(self.base_directory,'Basic_Information_Totals')
        file_loc=os.path.join(loc,'Labor_Rates.csv')
        f=open(file_loc,'r')
        f_data=f.readlines()
        f.close()
        names=[]
        for i in range(len(f_data)):
            names.append(f_data[i].split(sep=',')[0])
        #get the totals from the labor page
        individauls=self.labor.find_tech_individual()
        #combine the two lists into a single string
        combined=''
        for i in range(len(individauls)):
            combined+='{}: ${:,.2f}\n'.format(names[i],individauls[i])
        QMessageBox.information(self,'Labor Breakdown',combined,
                                            QMessageBox.Ok)
    def date_change(self):
        '''change the data on the invoices for the month
        '''
        self.date_changed=QWidget()
        self.date_changed.setWindowTitle('Change Invoice Date')
        self.date_changed.setWindowIcon(QIcon('BEI_Logo.png'))
        self.line=QLineEdit()
        self.line.setFont(self.font)
        self.line.setSizePolicy(self.size_policy,self.size_policy)
        self.save_date=QPushButton('Save Date')
        self.save_date.setFont(self.font)
        self.save_date.setSizePolicy(self.size_policy,self.size_policy)
        self.save_date.clicked.connect(self.saved_date)
        layout=QVBoxLayout()
        layout.addWidget(self.line)
        layout.addWidget(self.save_date)
        self.date_changed.setLayout(layout)
        
        d_location=os.path.join(self.base_directory,'Basic_Information_Totals')
        self.date_location=os.path.join(d_location,'Invoice_Date.txt')
        
        y=open(self.date_location,'r')
        date=y.readlines()
        y.close()
        self.line.setText(date[0])
        self.date_changed.show()
        
    def saved_date(self):
        '''
        Save the new date
        '''
        y=open(self.date_location,'w')
        y.write(self.line.text())
        y.close()
        self.date_changed.close()
        
    def new_job_nums(self):
        '''Run the class to create more job numbers 
        '''
        self.n_jobs=Job_Numbers()
        
    def cheat_sheet(self):
        '''Open the cheat sheet for viewing
        '''
        self.chea=Read_Cheat_Sheet(self.font,self.size_policy,
                                           self.base_directory)
        
    def add_cheat_task(self):
        self.cheat=Write_Cheat_Sheet(self.font,self.size_policy,
                                     self.base_directory)
    
    def partial_payment(self):
        self.a=Partial_Payments(self.font,self.size_policy)
        self.a.add.clicked.connect(self.proce)
        
    def proce(self):
        try:
            self.a.process()
            self.this_payment=self.a.amount
            try:
                location=os.path.join(os.path.join(self.base_directory,
                                           'Saved_Invoices'),
                                            '{}'.format(self.current_job))
                payments=os.path.join(location,'Payments.csv')
                f=open(payments,'r')
                value=float(f.readlines()[0])
                f.close()
                self.this_payment+=value
            except:
                self.this_payment=self.this_payment
            self.comments.append('''Partial payment of ${:,.2f} on {}, leaves a remaining balance of ${:,.2f}'''
                                 .format(self.a.amount,self.a.date,
                                         self.totals-self.a.amount))
            f=open(payments,'w')
            f.write(str(self.this_payment))
            self.partial=self.this_payment
            self.calculate_totals()
            f.close()
        except:
            pass
    def finance_charges(self):
        self.charg=Finance_Charges(self.font,self.size_policy)
        self.charg.add.clicked.connect(self.fin_process)
        
    def fin_process(self):
        self.charg.process()
        self.finance+=self.charg.amount
            
        self.comments.append('Finance Charge of ${:,.2f} applied on {}, kindly remit payment immediately.'.format(self.charg.amount,self.charg.date))
        location=os.path.join(os.path.join(self.base_directory,
                                           'Saved_Invoices'),
                                            '{}'.format(self.current_job))
        fin_loc=os.path.join(location,'Finance.csv')
        f=open(fin_loc,'w')
        f.write(str(self.finance))
        f.close()
        self.calculate_totals()
        
    def change_basic_info(self):
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
        flag=False
        #change the information in basic[2] and basic[3] to match the new values
        if basic[2].split(sep='\n')[0]!=self.machine.text():
            old=basic[2].split(sep='\n')[0].replace(' ','_')
            cust=basic[1].split(sep='\n')[0].replace(' ','_')
            file_name=basic[0].split(sep='\n')[0]+'.pdf'
            flag=True
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
            
        self.tax=float(self.tax_value.text())/100
        
        f=open(os.path.join(location,'Basic_Info.csv'),'w')
        for i in range(len(basic)):
            if '\n' not in basic[i]:
                f.write('{}\n'.format(basic[i]))
            else:
                f.write('{}'.format(basic[i]))
        f.close()
        
        #change the percent shown in the total value
        self.totals_table.tableWidget.setItem(5,0,
                                              QTableWidgetItem('Tax: {:.2f}%'
                                               .format(self.tax*100)))
        #next update the totals
        self.calculate_totals()
        self.save_invoice()
        time.sleep(3)
        if flag:
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
                
    def view_windows(self):
        '''Used to re-initialize the totals and main window'''
        self.save_invoice()
        self.read_in_data()
        
    def closeEvent(self,event):
        if self.start_flag:
            self.save_invoice(printing=True)
            flag=self.save_no_threading()
            if flag==0:
                reply=QMessageBox.question(self,'Close Window',
                                       'Do you want to close the application?',
                                       QMessageBox.Yes| QMessageBox.No, 
                                       QMessageBox.No)
                        #check to see if the program is up to date
                checker,new,current=VC.check(self.base_directory)
                if checker:
                    QMessageBox.information(self,'Software Version',
                    'Your software needs updated from version {} to version {}. Run BEI_Updater'.format(current,new),
                    QMessageBox.Ok)
                
                if reply==QMessageBox.Yes:
                    event.accept()
                else:
                    event.ignore()
            else:
                event.ignore()
        else:
            event.accept()
            
    def updater(self):
        QMessageBox.information(self,'Restart Required',
                                'Run BEI_Updater and Restart program',
                                QMessageBox.Ok)
#        self.close()
        
    def change_address(self):
        self.edi=EDI(self.font,self.size_policy,self.base_directory)
        
    def view_customer(self):
        flag=self.save_no_threading()
        if flag==0:
            location=os.path.join(os.path.expanduser('~/Desktop'),
                                  'BEI_Invoices')
            location=os.path.join(location,'Customer')
            cust_location=os.path.join(location,self.customer.replace(' ','_'))
            machine_location=os.path.join(cust_location,self.machine_text.replace(' ','_'))
            job_location=os.path.join(machine_location,
                                      '{}.pdf'.format(self.current_job)).replace('&','^&')
            print(job_location)
            subprocess.Popen(job_location,shell=True)
        else:
            pass
        
    def view_company(self):
        flag=self.save_no_threading()
        if flag==0:
            location=os.path.join(os.path.expanduser('~/Desktop'),
                                  'BEI_Invoices')
            location=os.path.join(location,'Company')
            cust_location=os.path.join(location,self.customer.replace(' ','_'))
            machine_location=os.path.join(cust_location,self.machine_text.replace(' ','_'))
            job_location=os.path.join(machine_location,
                                      '{}.pdf'.format(self.current_job)).replace('&','^&')
            subprocess.Popen(job_location,shell=True)
        else:
            pass

    def save_no_threading(self):
        self.save_invoice(printing=True)
        try:
            pdf2.PDF_Builder(self.current_job,
                                self.base_directory,'Company')
            pdf2.PDF_Builder(self.current_job,
                             self.base_directory,'Customer')
            return 0
        except:
            QMessageBox.information(self,'Opening Failure',
                                    'Close file and try again',QMessageBox.Ok)
            time.sleep(1)
            return 1
        
    def envelop_write(self):
        #navigate to the envelope folder
        loc=os.path.join(os.path.join(
                self.base_directory,'Customer_Envelopes'),
                self.envelope_date+'.env')
        f=open(loc,'r')
        data=f.readline()
        f.close()
        cust=data.split(sep=' ')
        cust.remove('')
        
        reply=QMessageBox.information(self,'Envelope Printing',
    'Load {} invoices into printer before clicking OK'.format(len(cust))
                                    ,QMessageBox.Ok)
        base=self.base_directory
        if reply==QMessageBox.Ok:
            for i in range(len(cust)):
                enve_loc=os.path.join(os.path.join(base,'Customer_Envelopes',
                                      cust[i]+'.pdf'))
                os.startfile(enve_loc,'print')
            
    def envelop_write1(self):
        #get the job number to print
        num,ok=QInputDialog.getText(self,'Single Customer Envelope',
                                    'Job Number to print:',QLineEdit.Normal,'')
        if num!='' and ok:
           writer=EWriter(self.base_directory,num)
           writer.generate_latex()
           QMessageBox.information(self,'Envelope Printing',
               'Load 1 envelope into printer before clicking OK',
               QMessageBox.Ok)
           writer.print_pdf()
   
    def billing_envelopes(self):
        self.billing_=CE(self.base_directory)
    
    def change_customer(self):
        changer=CC(self.base_directory,self.current_job)
        customers=changer.Customer()
        
        item,ok=QInputDialog.getItem(self,'New Customer','Listed Customers:'
                                     ,customers,0,False)
        if item and ok:
            changer.change_name(item)
        self.save_invoice(no_build=True)
        self.read_in_data()
            
if __name__=="__main__":
    app=QApplication(sys.argv)
    ex=Invoice()
    sys.exit(app.exec_())