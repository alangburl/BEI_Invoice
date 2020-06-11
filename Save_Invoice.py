import os, sys, psutil, subprocess

class Save_Invoice():
    def __init__(self, base_directory, current_job):
        self.base_directory=base_directory
        self.current_job=current_job
        self.location=os.path.join(os.path.join(self.base_directory,
                                   'Saved_Invoices'),self.current_job)
        
    def parts_saving(self, parts_table):
        self.parts=parts_table
        location=self.location
        parts_file=os.path.join(location,'Parts.csv')
        #first read and write the parts information
        f=open(parts_file,'w')
        row=[]
        for i in range(100):
            try:
                for j in range(8):
                    if j==0:
                        if self.parts.parts_table.tableWidget.item(i,j).text()!='*':
                            val=float(self.parts.parts_table.tableWidget.item(i,
                                                                      j).text())
                        elif self.parts.parts_table.tableWidget.item(i,j).text()=='*':
                            val=self.parts.parts_table.tableWidget.item(i,j).text()
                        row.append(val)
                    else:
                        try:
                            val=self.parts.parts_table.tableWidget.item(i,
                                                                    j).text()
                            row.append(val)
                        except:
                            row.append('')
                if '\n' in row[-1]:
                    row[-1]=row[-1].split(sep='\n')[0]
                row[2]=row[2].replace(',','.')
                f.write('{},{},{},{},{},{},{},{}\n'.format(*row))
                row=[]
            except:
                break
        f.close()
        
    def total_table(self, t_row):
        total_location=os.path.join(self.location,'Totals.csv')
        h=open(total_location,'w')
        for i in t_row:
            try:
                float(i)
                h.write('{:.2f}\n'.format(i))
            except:
                h.write('0')
        h.close()
        
    def comments(self,comments):
        comments_location=os.path.join(self.location,'Comments.csv')
        v=open(comments_location,'w')
        v.write(comments.toPlainText())
        v.close()     
        
    def labor_saving(self,labor):
        count=labor.counts
        for l in range(count):
            labor_location=os.path.join(self.location,'tech{}.csv'.format(l))
            o=open(labor_location,'w')
            #get the data from the labor class
            tech_labor=labor.read_data_out(l)
            for k in range(len(tech_labor)):
                if '\n' in list(tech_labor[k][-1]):
                    tech_labor[k][-1]=float(tech_labor[k][-1])
                o.write('{},{},{},{},{},{},{},{}\n'.format(*tech_labor[k]))
            o.close()
            
    def pdf_shut(self):
        acrobat='Acrobat.exe' in (p.name() for p in psutil.process_iter())
        reader='AcroRd32.exe' in (p.name() for p in psutil.process_iter())
        if acrobat:
            lis=['taskkill','/F','/IM','Acrobat.exe','/T']
            subprocess.call(lis)
        if reader:
            os.system('taskkill /F /IM "AcroRd32.exe" /T')
    