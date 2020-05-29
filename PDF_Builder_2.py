#updated PDF builder to reduce down to one class instead of two
import os, sys,subprocess,shutil,time
from pathlib import Path
from PyQt5.QtWidgets import QMessageBox,QWidget
class PDF_Builder():
    '''Build a PDF table of the data in the tables provided
    Steps this function does:
        1.) Takes arguements of in the form of lists for:
                parts, totals, and basic_information. And as a string:
                base_directory
        Function: preface_builder
        2.) Reads the template and divides it into the lines
        3.) Replaces the empty fields with information from basic_information
                Items to be replaced:
                    Job Number:
                    Machine:
                    Customer:
                    Address line 2:
                    Address line 3:
                    Date:
        Function: table_builder
        4.) Build the header for the Company and Customer page
        5.) Places the entries from [parts] in the correct locations for 
            their respective pages
        Function: notes
        6.) Places any pertinent notes in the field of the table
        Function: comments
        7.) Puts the comments some in the footer
        8.) Places the totals table next to the comments
        Function: build
        9.) Builds the customer and company copies of the invoice 
    '''
    def __init__(self,job_num,base_directory,comp_cust):
        super().__init__()
        #these are the same information for the customer as for the company
        self.base_directory=base_directory
        self.location=os.path.join(os.path.join(base_directory,
                                                'Saved_Invoices'),str(job_num))
        self.preface_data_read_in()
        
        ###
        if comp_cust=='Company':
            self.preface_builder('Company')
            self.parts_read_in('Company')
            self.total_comments()
            self.tex_builder('Company')
        elif comp_cust=='Customer':
            self.preface_builder('Customer')
            self.parts_read_in('Customer')
            self.total_comments()
            self.tex_builder('Customer')            
    
    def preface_data_read_in(self):
        '''Read the data from the basic info file
        '''
        f=open(os.path.join(self.location,'Basic_Info.csv'),'r')
        data=f.readlines()
        f.close()
        self.basic_info=[]
        for i in range(len(data)):
            if i!=3:
                self.basic_info.append(data[i].split(sep='\n')[0])
            elif i==3:
                self.tax_percentage=float(data[i].split(sep=',')[0])*100
                try:
                    self.tax_code=data[i].split(sep=',')[1].split(sep='\n')[0]
                except:
                    self.tax_code=''
        #get the invoice date
        d_location=os.path.join(self.base_directory,'Basic_Information_Totals')
        date_location=os.path.join(d_location,'Invoice_Date.txt')
        t=open(date_location,'r')
        self.date=t.readlines()[0]
        t.close()
    def preface_builder(self,version):
        '''Define the preface of each pdf
        '''
        #get the lines from template
        p=open(os.path.join(os.path.join(self.base_directory,'Built_Invoices'),
                            'preface_template.tex'),'r')
        if version=='Company':
            pref=p.readlines()[0:-2]
        elif version=='Customer':
            pref=p.readlines()
        p.close()
        preface_data=[]
        for i in pref:
            preface_data.append(i.split(sep='\n')[0])
            
        self.replace1=['@','#','$','%','&']
        mach=self.basic_info[2]
        cust=self.basic_info[1]
        for i in self.replace1:
            mach=mach.replace(i,r'\{}'.format(i))
            cust=cust.replace(i,r'\{}'.format(i))
            
        #read in the data missing from the preface document
        additional_data=[r'\begin{document}',
                         r'\begin{centering}',
                         r'{\LARGE Burl Equipment Inc} \\',
                         r'P.O. Box 347\\',
                         r'Cimarron, Ks 67835\\',
                         r'620-855-3871\\',
                         r'\end{centering}',
                         r'\begin{multicols}{2}',
                         r'\begin{flushleft}',
                         r'\begin{tabular}{ll}',
                         r'Job Number: &{}\\'.format(self.basic_info[0]),
                         r'Machine: &{} \\'.format(mach),
                         r'Customer: &{} \\'.format(cust),
                         r' & {}\\'.format(self.basic_info[3]),
                         r' & {}\\'.format(self.basic_info[4]),
                         r'\end{tabular}',
                         r'\end{flushleft}',
                         r'\columnbreak',
                         r'\vfill',
                         r'\flushright',
                         r'Date: {}'.format(self.date),
                         r'\end{multicols}'
                         ]
        #combine the file back together
        self.header=preface_data+additional_data
        
    def parts_read_in(self,version):
        '''Read the parts file in
        '''
        if version=='Company':
            line3=r'\begin{longtable}{@{\extracolsep{\fill}}llp{9cm}rrr@{\extracolsep{\fill}}}'
            line5=r'Qty & Part Number & Description & Cost & Price & Extension\\* \midrule'
        elif version=='Customer':
            line3=r'\begin{longtable}{@{\extracolsep{\fill}}llp{10cm}rr@{\extracolsep{\fill}}}'
            line5=r'Qty & Part Number & Description & Price & Extension\\* \midrule'
        
        p=open(os.path.join(self.location,'Parts.csv'),'r')
        p_data=p.readlines()
        p.close()
        parts_data=[
                    r'\setlength\LTleft{0pt}',
                    r'\setlength\LTright{0pt}',
                    line3,
                    r'\toprule',
                    line5,
                    r'\endhead'
                    ]
        for i in range(len(p_data)):
            dat=p_data[i].split(sep=',')[0:6]
            try:
                dat[-1]=float(dat[-1])
            except:
                dat[-1]=dat[-1]
            try:
                dat[-2]=float(dat[-2])
            except:
                dat[-2]=dat[-2]
            if version=='Company':
                try:
                    dat[-3]=float(dat[-3])
                except:
                    dat[-3]=dat[-3]
            elif version=='Customer':
                try:
                    float(dat[-3])
                    dat.remove(dat[-3]) 
                except:
                    dat.pop(-3)      
            put_and=''
            for j in dat:
                if type(j)==float:
                    put_and+='{:,.2f}&'.format(j)
                else:
                    for i in self.replace1:
                        j=j.replace(i,r'\{}'.format(i))
                    put_and+='{}&'.format(j)
            parts_data.append(r'{}\\'.format(put_and[0:-1]))
        parts_data.append(r'\end{longtable}')
        self.header+=parts_data
        
    def total_comments(self):
        '''Build the totals table and add the comments
        '''
        #open the totals and read them in
        u=open(os.path.join(self.location,'Totals.csv'))
        t_data=u.readlines()
        u.close()
        totals_=[float(i.replace('\n','')) for i in t_data]
        
        #read in the comments
        c=open(os.path.join(self.location,'Comments.csv'))
        c_data=c.readlines()
        c.close()
        
        comments_=[i.replace('\n',r'\\') for i in c_data]

        for i in range(len(comments_)):
            for j in self.replace1:
                comments_[i]=comments_[i].replace(j,r'\{}'.format(j))
    
        totals_comments=[
                        r'\vspace{\fill}',
                        r'\noindent',
                        r'\begin{minipage}{\textwidth}',
                        r'\begin{minipage}[b][][t]{0.7\textwidth}'
                        ]
        for k in comments_:
            totals_comments.append(k)
        totals_comments.append(r'\end{minipage}%')
        totals_comments.append(r'\begin{minipage}[b][][t]{0.3\textwidth}')
        
        tots=[r'\begin{flushright}',
              r'\begin{tabular}{lr}',
              r'Parts & \${:,.2f}\\'.format(totals_[0]),
              r'Labor & \${:,.2f}\\'.format(totals_[1]),
              r'Supplies & \${:,.2f}\\'.format(totals_[2]),
              r'Freight & \${:,.2f}\\'.format(totals_[3]),
              r'Subtotal & \${:,.2f}\\'.format(totals_[4]),
              r'Tax {} {:.2f}\% & \${:,.2f}\\'.format(self.tax_code,
                    self.tax_percentage,totals_[5]),
              r'\textbf{TOTAL}'+ r'& \${:,.2f}\\'.format(totals_[6]),
              r'\end{tabular}',
              r'\end{flushright}'
              r'\end{minipage}\\ \\'
                ]
        self.header+=totals_comments
        self.header+=tots

    def tex_builder(self,version):
       '''Build the table
       '''
       self.header.append(r'\noindent TERMS: Due 10 days from receipt of invoice. A late fee of 2\% (\$5.00 minimum) per month will be charged to all past due invoices. Please pay from invoice as no statement will be sent.')
       self.header.append(r'\end{minipage}')
       self.header.append(r'\end{document}')
       #write the data back out to the desktop folder
       location=os.path.join(os.path.expanduser('~/Desktop'),'BEI_Invoices')
       location=os.path.join(location,version)
       f=open(os.path.join(location,'{}.tex'.format(
            self.basic_info[0])),'w')
       for i in self.header:
           f.write(i+'\n')
       f.close()
       tex_location=os.path.join(location,'{}.tex'.format(self.basic_info[0]))
       startupinfo = subprocess.STARTUPINFO()
       startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
       
       if version=='Customer':
           subprocess.call(['pdflatex',tex_location],startupinfo=startupinfo)
           subprocess.call(['pdflatex',tex_location],startupinfo=startupinfo)
       if version=='Company':
           subprocess.call(['pdflatex',tex_location],startupinfo=startupinfo)

       
       #make/check if the directory BEI_Invoices-Company-CustomerName-Machine
       #exists, if not create it and save the pdf there
       #first change the customer and machine names into easy names
       new_customer=self.basic_info[1].replace(' ','_')
       new_machine=self.basic_info[2].replace(' ','_')
       new_location=os.path.join(os.path.join(location,new_customer),
                                 new_machine)
       #get the current directorys in location
       directories=os.listdir(location)
       #check to see if the directory location-new_customer-new_machine exists
       if new_customer not in directories:
           os.mkdir(os.path.join(location,new_customer))
       #check to see if the machine is in location-new_customer
       if new_machine not in os.listdir(os.path.join(location,new_customer)):
           os.mkdir(new_location)
           
       current_location=os.path.join(os.getcwd(),
                                     '{}.pdf'.format(self.basic_info[0]))
       #shut the pdf in the bei folder to ensure proper writing is possible
       self.new_loc=shutil.move(current_location,os.path.join(new_location,
                                         '{}.pdf'.format(self.basic_info[0])))
       
       self.new_loc=os.path.join(new_location,
                                         '{}.pdf'.format(self.basic_info[0]))
       
       #remove the two wasted files from code directory
       os.unlink(os.path.join(os.getcwd(),'{}.log'.format(self.basic_info[0])))
       os.unlink(os.path.join(os.getcwd(),'{}.aux'.format(self.basic_info[0])))
#       os.unlink(tex_location)
       
    def print_tex(self):
        '''Actually print the document
        '''
        os.startfile(self.new_loc,'print')