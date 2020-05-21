'''Create a GUI to launch the python script used to determine build the 
    invoices. I am using this and will port it to an exe file using pyinstaller
    instead of having to rebuild the entire system everytime a change is needed
    '''
#prefined imports
import os,subprocess,time,shutil

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
#        try:
        try:
            os.system('taskkill /F /IM "BEI_Invoice.exe" /T')
            time.sleep(2)
        except:
            False
        self.file_pull()
        self.recreate_exe()
        self.copy_picture()
            
#        except:
#            print('Update failed')
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
        
    def copy_picture(self):
        copy=['BEI_Logo.png','loader_image.png','bei_icon.ico']
        dire=os.getcwd()
        
        dest=os.path.join(os.path.join(dire,'dist'),'BEI_Invoice')
        for i in copy:
            shutil.copy2(i,os.path.join(dest))
        print('Update successful')
    
    
if __name__=="__main__":
    Launcher()