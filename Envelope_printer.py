import os
class Envelope_Printer():
    def __init__(self,base_directory,customer,job_number):
        self.base_directory=base_directory
        self.customer=customer.replace(' ','_')
        self.current_job=job_number
        if 'Customer_Envelopes' not in os.listdir(self.base_directory):
            os.mkdir(os.path.join(self.base_directory,'Customer_Envelopes'))
        dire=os.path.join(self.base_directory,'Customer_Envelopes')
        
        #then either make or open the date file
        #get the current date for the invoices
        loc=os.path.join(self.base_directory,'Basic_Information_Totals')
        loc2=os.path.join(loc,'Invoice_Date.txt')
        file=open(loc2,'r')
        date=file.readlines()[0].replace('/','_')
        self.date=date
        file.close()
        #then read the file, then check and see if the customer is 
        #already in the list for this month
        dire=os.path.join(dire,date+'.env')
                try:
            file2=open(dire,'r')
            data=file2.readline()
            file2.close()
            
            cust=data.split(sep=' ')
            if self.customer not in cust:
                cust.append(self.customer)
            
            cust.remove('')
            file2=open(dire,'w')
            for j in cust:
                file2.write(j+' ')
            file2.close()
            
        except:
            file2=open(dire,'w')
            file2.write('{} '.format(self.customer))
        #close the envelopes file and wait for the next go around
        file2.close()
        
    def dater(self):
        return self.date
        