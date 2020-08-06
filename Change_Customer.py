import os,shutil

class Change_Customer:
    def __init__(self, base_directory, job_number):
        self.base_directory=base_directory
        job_number=job_number.replace(' ','_')
        self.job=job_number
        self.directory=os.path.join(
                os.path.join(base_directory,'Saved_Invoices'),job_number)
        
    def Customer(self):
        #first get a list of customers to populate the list with 
        li=os.path.join(
                os.path.join(self.base_directory,
                             'Customer_Information'),
                             'Customers.txt')
        f=open(li,'r')
        dat=f.readlines()
        f.close()
        data=[]
        for i in dat:
            data.append(i.split(sep='\n')[0])
        return data
        
    def change_name(self,new_customer):
        file=os.path.join(self.directory,'Basic_Info.csv')
        f=open(file,'r')
        data=f.readlines()
        f.close()
        
        #need to also get the updated address for the customer
        li=os.path.join(
                os.path.join(self.base_directory,
                             'Customer_Information'),
                             'Addresses')
        pathr=os.path.join(li,new_customer.replace(' ','_')+'.txt')
        f=open(pathr,'r')
        add=f.readlines()
        f.close()
        
        g=open(file,'w')
        self.old_customer=data[1].split(sep='\n')[0]
        self.machine=data[2].split(sep='\n')[0].replace(' ','_')
        data[1]=new_customer+'\n'
        data[4]=add[0]
        data[5]=add[1]
        for i in data:
            g.write(i)
        g.close()
        
        self.remove_old_job()
        
    def remove_old_job(self):
        #take care of the previously saved information
        #first get the correct directory
        location=os.path.join(os.path.expanduser('~/Desktop'),'BEI_Invoices') 
        company=os.path.join(location,'Company')
        customer=os.path.join(location,'Customer')
        
        cust=self.old_customer.replace(' ','_')
        com=os.path.join(os.path.join(company,cust),self.machine)
        cus=os.path.join(os.path.join(customer,cust),self.machine)
        if len(os.listdir(cus))==1:
            shutil.rmtree(com)
            shutil.rmtree(cus)
        else:
            loc_comp=os.path.join(com,self.job+'.pdf')
            loc_cust=os.path.join(cus,self.job+'.pdf')
            os.unlink(loc_comp)
            os.unlink(loc_cust)
        
        