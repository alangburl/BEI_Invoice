import PDF_Builder_2 as PDF

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
            PDF.PDF_Builder(self.job,self.loc,'Company')
            PDF.PDF_Builder(self.job,self.loc,'Customer')
        except:
            self.out.emit(1)