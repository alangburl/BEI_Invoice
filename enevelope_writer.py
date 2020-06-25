#enevelope file generation
import os,shutil,subprocess
class Enevelope_Writer():
    def __init__(self,base_directory,job_number):
        save=os.path.join(base_directory,'Saved_Invoices')
        job=os.path.join(os.path.join(save,job_number),'Basic_Info.csv')
        self.job=os.path.join(save,job_number)
        self.saving=os.path.join(base_directory,'Customer_Envelopes')
        f=open(job,'r')
        self.data=f.readlines()
        f.close()
        
    def generate_latex(self):
        replace=['@','#','$','%','&']
        customer=self.data[1].split('\n')[0]
        self.customer=customer.replace(' ','_')
        tex_name=self.customer+'.tex'
        address1=self.data[4].split('\n')[0]
        address2=self.data[5].split('\n')[0].replace(',',' ')
        tex_location=os.path.join(self.saving,tex_name)
        file=open(tex_location,'w')
        header_return=[r'\documentclass{letter}'
                r'\usepackage{graphics}',
                r'\usepackage[businessenvelope]{envlab}',
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
        os.unlink(os.path.join(os.getcwd(),'{}.aux'.format(self.customer)))
        os.unlink(os.path.join(os.getcwd(),'{}.log'.format(self.customer)))
        
        shutil.move(os.path.join(os.getcwd(),'{}.pdf'.format(self.customer)),
                    os.path.join(self.saving,'{}.pdf'.format(self.customer)))
        os.unlink(os.path.join(self.saving,tex_name))
        
    def print_pdf(self):
        loc=os.path.join(self.saving,'{}.pdf'.format(self.customer))
        os.startfile(loc,'print')
        
if __name__=="__main__":
    Enevelope_Writer(r"C:\Users\alang\BEI_Invoices",'123')