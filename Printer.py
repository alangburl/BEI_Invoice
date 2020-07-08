import win32print as win
import win32api as api

class Printer():
    def __init__(self, file):
        name=win.GetDefaultPrinter()
        printdefaults={"DesiredAccess": win.PRINTER_ALL_ACCESS}
        handle=win.OpenPrinter(name,printdefaults)
        
        level=2
        attributes=win.GetPrinter(handle,level)
        attributes['pDevMode'].Duplex=1
        win.SetPrinter(handle,level,attributes,0)
        win.GetPrinter(handle,level)['pDevMode'].Duplex
        api.ShellExecute(0,'print',file,'.','/manualstoprint',0)
        return 0