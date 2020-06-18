import os,subprocess

def check(base_directory):
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    subprocess.call(['git','pull'])
    try:
        base=os.path.join(base_directory,'Log')
        dire=os.path.join(base,'current.ver')
        f=open(dire,'r')
        current_version=f.readlines()[0]
        f.close()
        f=open('new.ver','r')
        new_version=f.readlines()[0]
        f.close()
        
        if current_version!=new_version:
            return True, new_version,current_version
    except:
        return False,0,0