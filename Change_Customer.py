import os

class Change_Customer:
    def __init__(self, base_directory, job_number):
        self.base_directory=base_directory
        job_number=job_number.replace(' ','_')
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
        data[1]=new_customer+'\n'
        data[4]=add[0]
        data[5]=add[1]
        for i in data:
            g.write(i)
        g.close()
        
        
        