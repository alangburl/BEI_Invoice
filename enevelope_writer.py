#enevelope file generation
import os,shutil,subprocess
class Enevelope_Writer():
    def __init__(self,base_directory,job_number):
        self.base_directory=base_directory
        save=os.path.join(base_directory,'Saved_Invoices')
        job=os.path.join(os.path.join(save,job_number),'Basic_Info.csv')
        self.job=os.path.join(save,job_number)
        f=open(job,'r')
        self.data=f.readlines()
        f.close()
        
    def generate_latex(self):
        replace=['@','#','$','%','&']
        customer=self.data[1].split('\n')[0]
        self.customer=customer.replace(' ','_')
        address1=self.data[4].split('\n')[0]
        address2=self.data[5].split('\n')[0].replace(',',' ')
        tex_name=self.customer+'.tex'
        tex_location=os.path.join(self.job,tex_name)
        file=open(tex_location,'w')
        header_return=[r'\documentclass{letter}',
                r'\usepackage{graphics}',r'\usepackage[businessenvelope]{envlab}',
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
        os.unlink(os.path.join(os.getcwd(),self.customer+'.aux'))
        os.unlink(os.path.join(os.getcwd(),self.customer+'.log'))
        new_loc=os.path.join(os.path.join(self.base_directory,
                          'Customer_Envelopes'),self.customer+'.pdf')
        shutil.move(os.path.join(os.getcwd(),self.customer+'.pdf'),new_loc)
        os.unlink(os.path.join(self.job,tex_name))
        
    def print_pdf(self):
        loc=os.path.join(self.job,self.customer+'.pdf')
        os.startfile(loc,'print')
        
if __name__=="__main__":
    Enevelope_Writer(r"C:\Users\alang\BEI_Invoices",'123')