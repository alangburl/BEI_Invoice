#enevelope file generation
import os,shutil,subprocess
class Enevelope_Writer():
    def __init__(self,base_directory,job_number):
        save=os.path.join(base_directory,'Saved_Invoices')
        job=os.path.join(os.path.join(save,job_number),'Basic_Info.csv')
        self.job=os.path.join(save,job_number)
        f=open(job,'r')
        self.data=f.readlines()
        f.close()
        
    def generate_latex(self):
        replace=['@','#','$','%','&']
        customer=self.data[1].split('\n')[0]
        address1=self.data[4].split('\n')[0]
        address2=self.data[5].split('\n')[0].replace(',',' ')
        tex_location=os.path.join(self.job,'envelope.tex')
        file=open(tex_location,'w')
        header_return=[r'\documentclass{letter}',r'\usepackage{geometry}',
                r'\geometry{paperheight=220mm,paperwidth=110mm}',
                r'\usepackage{graphics}',r'\usepackage{envlab}',
                r'\SetEnvelope{220mm}{110mm}',
                r'\setlength{\ToAddressTopMargin}{20mm}',
                r'\setlength{\ToAddressLeftMargin}{20mm}',
                r'\makelabels',r'\begin{document}',
                r'\startlabels',
                r'\mlabel{Burl Equipment Inc\\ PO Box 347\\ Cimarron KS 67835}{']
        
        for i in header_return:
           file.write(i+'\n')
        customer1=customer
        for i in replace:
            customer1=customer1.replace(i,r'\{}'.format(i))
        file.write(r'{}\\{}\\{}'.format(customer1,address1,address2))
        file.write(r'}')
        file.write(r'\end{document}')
        file.close()
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        subprocess.call(['pdflatex',tex_location],startupinfo=startupinfo)
        os.unlink(os.path.join(os.getcwd(),'envelope.aux'))
        os.unlink(os.path.join(os.getcwd(),'envelope.log'))
        
        shutil.move(os.path.join(os.getcwd(),'envelope.pdf'),
                    os.path.join(self.job,'envelope.pdf'))
        os.unlink(os.path.join(self.job,'envelope.tex'))
        
    def print_pdf(self):
        loc=os.path.join(self.job,'envelope.pdf')
        os.startfile(loc,'print')
        
if __name__=="__main__":
    Enevelope_Writer(r"C:\Users\alang\BEI_Invoices",'123')