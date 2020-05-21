'''Create a GUI to launch the python script used to determine build the 
    invoices. I am using this and will port it to an exe file using pyinstaller
    instead of having to rebuild the entire system everytime a change is needed
    '''
#prefined imports
import os,subprocess,time

class Launcher():
    '''Runs the main window of the invoice development
    Calls the table to be used for parts and labor from
    table_widget.py
    '''
    def __init__(self):
        '''
            Call the function to launch the GUI
        '''
        super().__init__()
        try:
            os.system('taskkill /F /IM "BEI_Invoice.exe" /T')
            self.file_pull()
            
        except:
            pass
        time.sleep(2)
        
    def file_pull(self):
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        subprocess.call(['git','pull'])
        
    def recreate_exe(self):
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        subprocess.call(['pyinstaller','BEI_Invoice.py',
                         '--windowed','--noconfirm'])     
        
        copy=['BEI_Logo.png','bei_logo_R5r_icon.ico','loader_image.png']
        dire=os.getcwd()
        
        dest=os.path.join(os.path.join(dire,'dist'),'BEI_Invoice')
        for i in copy:
            subprocess.call(['cp',os.path.join(dire,i), os.path.join(dest,i)])
    
    
if __name__=="__main__":
    Launcher()