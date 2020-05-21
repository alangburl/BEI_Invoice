import os
class Old_Job_Converter():
    def __init__(self,base_directory,old_invoice,matrix,checker):
        super().__init__()
        self.base_directory=base_directory
        self.save_location=os.path.join(self.base_directory,'Saved_Invoices')
        self.old_invoice=old_invoice
        self.matrix=matrix
        self.checker=checker
#        self.read_excel()
        self.populate_basic_info()
        self.populate_part_info()
        self.populate_total_info()
        self.populate_comment_info()
    def read_excel(self):
        '''Read the excel document and get the data into a readable form'''
#        book=pd.read_excel(self.old_invoice)
#        self.matrix=book.values.tolist()
        self.retrieve_basic_info()
        self.retrieve_part_info()
        
    def retrieve_basic_info(self):
        self.job_num=self.matrix[6][1]
        self.machine=self.matrix[7][1]
        self.customer=self.matrix[8][1]
        self.address1=self.matrix[9][1]
        self.address2=self.matrix[10][1]
        self.save_location=os.path.join(self.save_location,str(self.job_num))
        try:
            os.mkdir(self.save_location)
        except:
            True
    
    def retrieve_part_info(self):
        self.qty=[]
        self.part_number=[]
        self.description=[]
        self.cost=[]
        self.price=[]
        self.extension=[]
        self.freight=[]
        self.misc=[]
        self.start=0
        end=0
        #first find the start and end lines
        for i in range(len(self.matrix)):
            try:
                if 'Qty:' in self.matrix[i][0]:
                    start=i
                elif 'Comments:' in self.matrix[i][0]:
                    end=i
            except:
                True
        for i in range(start+1,end):
            self.qty.append(self.matrix[i][0])
            self.part_number.append(self.matrix[i][1])
            self.description.append(self.matrix[i][2])
            self.cost.append(self.matrix[i][3])
            self.price.append(self.matrix[i][5])
            self.extension.append(self.matrix[i][6])
            self.freight.append(self.matrix[i][7])
            try:
                self.misc.append(self.matrix[i][8])
            except:
                self.misc.append(' ')
        self.comments=self.matrix[end+1][0]   
        
        #now retrieve the totals from the cells
        self.totals=[]
        for i in range(end,len(self.matrix)-2):
            if 'Tax' in self.matrix[i][3]:
                self.tax_value=self.matrix[i][5]
                if self.tax_value!=0:
                    self.tax_code=self.matrix[i][3].split(sep='Tax ')[1]
                else:
                    self.tax_code=''
            self.totals.append(self.matrix[i][6])
        
    def populate_basic_info(self):
        basic_info=os.path.join(self.save_location,'Basic_Info.csv')
        basic=open(basic_info,'w')
        basic_=[self.job_num,str(self.customer).replace('#',''),self.machine,
                [self.tax_value,self.tax_code],self.address1,self.address2]
        for i in range(len(basic_)):
            if i!=3:
                basic.write('{}\n'.format(basic_[i]))
            else:
                basic.write('{},{}\n'.format(*basic_[3]))
        basic.close()
        
    def populate_part_info(self):
        parts_info=os.path.join(self.save_location,'Parts.csv')
        parts=open(parts_info,'w')
        for i in range(len(self.qty)):
            line=[self.qty[i],self.part_number[i],self.description[i],
                  self.cost[i],self.price[i],self.extension[i],
                  self.freight[i],self.misc[i]]
            
            line[2]=str(line[2]).replace(',','.').replace('$',
                                '/$').replace('&','and')
            for j in range(len(line)):
                try:
                    val=self.checker(line[j])
                    if val:
                        line[j]=' '
                except:
                    False

                
            if line[0]!='*' or type(line[0])==int or type(line[1])==float:
                parts.write('{},{},{},{},{},{},{},{}\n'.format(*line))
        parts.close()
        
    def populate_total_info(self):
        totals_info=os.path.join(self.save_location,'Totals.csv')
        totals=open(totals_info,'w')
        for i in self.totals:
            totals.write('{:.2f}\n'.format(i))
        totals.close()
        
    def populate_comment_info(self):
        comments_info=os.path.join(self.save_location,'Comments.csv')
        comments=open(comments_info,'w')
        if type(self.comments)==str:
            comments.write('Comments: '+self.comments)
        else:
            comments.write('Comments: ')
        comments.close()
                
if __name__=='__main__':
    a=Old_Job_Converter(r'C:\Users\alang\BEI_Invoices',
                      r"C:\Users\alang\Desktop\BEI_Invoices_Rev4\Code_Documents\Test_Documents\BEI_Invoice.xlsm.xlsx")
    dat=a.matrix