import PDF_Builder

from PyQt5.QtCore import QThread, pyqtSignal

class Saver(QThread):
    '''Threading the saving process
    '''
    out=pyqtSignal(int)
    def __init__(self,parent,directory,job_number):
        '''Used to save the invoice to a PDF
        '''
        QThread.__init__(self,parent=parent)
        self.loc=directory
        self.job=job_number
        
    def run(self):
        try:
            PDF_Builder.PDF_Builder_Company(self.job,self.loc)
            PDF_Builder.PDF_Builder_Customer(self.job,self.loc)
        except:
            self.out.emit(1)