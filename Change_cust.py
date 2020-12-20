class Basic_Updater():
    def __init__(self,file,info_dictionary):
        super().__init__()
        d=open(file,'r')
        data=d.readlines()
        d.close()
        
        for i in list(info_dictionary.keys()):
            if i=='tax':
                data[3]='{},{}\n'.format(*info_dictionary[i])
            if i=='customer':
                data[1]=info_dictionary[i][0]+'\n'
                data[4]=info_dictionary[i][1]+'\n'
                data[5]=info_dictionary[i][2]
            if i=='machine':
                data[2]=info_dictionary[i]+'\n'
                
        o=open(file,'w')
        for i in range(len(data)):
            o.write(data[i])
        o.close()
        
import os       
class Remove_Old():
    def __init__(self,cus_machine_job):
        super().__init__()
        location=os.path.join(os.path.expanduser('~/Desktop'),
                                  'BEI_Invoices')
        cust=os.path.join(location,'Customer')
        comp=os.path.join(location,'Company')
        
        cust=os.path.join(cust, cus_machine_job)
        comp=os.path.join(comp,cus_machine_job)
        
        os.unlink(cust)
        os.unlink(comp)
        
        
        