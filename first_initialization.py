import os
from pathlib import Path

class First_Run():
    def __init__(self,base_directory):
        super().__init__()
        self.base_directory=base_directory
        self.setup_folders()
        self.setup_files()
        self.preface_writer()
        
    def setup_folders(self):
        os.mkdir(str(Path(self.base_directory)))
        os.mkdir(os.path.join(str(Path(self.base_directory))
             ,'Saved_Invoices'))
        os.mkdir(os.path.join(str(Path(self.base_directory))
             ,'Built_Invoices'))
        os.mkdir(os.path.join(str(Path(self.base_directory))
             ,'Basic_Information_Totals'))
        os.mkdir(os.path.join(str(Path(self.base_directory))
             ,'Cheat_Sheets'))
        os.mkdir(os.path.join(str(Path(self.base_directory))
             ,'Customer_Information'))
        os.mkdir(os.path.join(os.path.join(str(Path(self.base_directory))
             ,'Customer_Information'),'Addresses'))
        os.mkdir(os.path.join(os.path.join(str(Path(self.base_directory))
             ,'Customer_Information'),'Machines'))

        bei=os.path.join(os.path.expanduser('~/Desktop'),'BEI_Invoices')
        os.mkdir(bei)
        os.mkdir(os.path.join(bei,'Customer'))
        os.mkdir(os.path.join(bei,'Company'))
        os.mkdir(os.path.join(bei,'Job_Numbers'))
        
    def setup_files(self):
        f=open(os.path.join(os.path.join(str(Path(self.base_directory))
             ,'Customer_Information'),'Customers.txt'),'w')
        f.close()        
        h=open(os.path.join(os.path.join(self.base_directory,
                         'Basic_Information_Totals'),'Invoice_Date.txt'),'w')
        h.write('1/1/2020')
        h.close()
        k=open(os.path.join(os.path.join(self.base_directory,
                         'Basic_Information_Totals'),'Labor_Rates.csv'),'w')
        k.write('Butch,90,120\nDavid,90,120\nAlan,90,120\nHanna,45,100')
        k.close()
        
        c=open(os.path.join(os.path.join(self.base_directory,'Cheat_Sheets'),
                            'Topics.txt'),'w')
        c.close()

    def preface_writer(self):
        loc=os.path.join(os.path.join(self.base_directory,'Built_Invoices'),
                         'preface_template.tex')
        p=open(loc,'w')
        values=[r'\documentclass[12pt]{article}',
                r'\usepackage{amsmath}',
                r'\usepackage{gensymb}',
                r'\usepackage[utf8]{inputenc}',
                r'\usepackage{setspace}',
                r'\usepackage[a4paper,top=0.5in,bottom=0.5in,inner=0.25in,outer=0.25in,footskip=0.25in]{geometry}',
                r'\usepackage{graphicx}',
                r'\usepackage{mathptmx}',
                r'\usepackage{booktabs}',
                r'\usepackage{cite}',
                r'\usepackage[english]{babel}',
                r'\usepackage{multicol}',
                r'\usepackage{transparent}',
                r'\usepackage{longtable}',
                r'\usepackage{background}',
                r'\backgroundsetup{scale=1,color=black,opacity=0.3,angle=0,contents={\includegraphics[width=0.5\linewidth]{loader_image}}}']
        for i in values:
            p.write(i+'\n')
        p.close()
        
if __name__ =="__main__":
    base_directory=str(Path(
                os.path.join(os.environ['USERPROFILE'],'BEI_Invoices')))
    First_Run(base_directory)