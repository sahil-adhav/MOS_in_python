data = '' #main memory in  list
second_block=0 
first_block=0
i=0     #file point
SI=0    #service interrupt
number_inst=0   #kitnegdpdH
IC=0            #instructioncounter
register=""     #register
flag=0          #toompareinCR
total_data_count=0      #to_check_number_of_data_cards_correct
AMJdata=" "              
jobid_check=1           #TO check job id     


data=[[],[],[],[],[],[],[],[],[],[],]
for x in range(10):
    for y in range(10):
        data[x].append([])  
        
        
try:
    f=open("python_output.txt","r+")
    f.truncate(0)
    f.close()    
except:
    pass


    

def terminate():
    display()
    print("execution completed\n\n")
    


def MOS(loc):
    global SI
    
    if SI==1:
        read(loc)
        SI=0
        
    if SI==2:
        write(loc)
        SI=0
        
    if SI==3:
        terminate()
        SI=0
    


    

def write(loc):
    file2=open("python_output.txt",'a')
    fb=int(loc[0])
    sb=int(loc[1])
    for sb in range(10):
        if data[fb][sb]==[]:
            continue
        
        file2.write(str(data[fb][sb]))
    file2.write("\n")
    print("written at",loc,"\n\n")
    
    
    
    
def read(loc):
        global total_data_count
        global i
        global AMJdata
        total_data_count=total_data_count+1
        if(total_data_count<=int(AMJdata)):
            fb=0
            sb=0
            j=0
            message=""
            fb=int(loc[0])  #1
            sb=int(loc[1])  #0
            if (fp[i]=="\n"):
                i=i+1
            while(fp[i]!="\n"):
                message=message+fp[i]
                i=i+1
            for sb in range((len(message)//4)+1):
                t=message[j:j+4]
                j=j+4
                data[fb][sb]=t
            print("read at ",loc,"\n\n")
        else:
            print("Wrong number of data card written")
            exit()
        


def execute():
    global second_block
    global first_block
    global data
    global SI
    global number_inst
    global IC
    global register
    global flag
    IC=0

    temp_IC=" "
    
    while(IC < number_inst):
        if  IC>9:
            temp_IC=str(IC)
            fb=int(temp_IC[0])
            sb=int(temp_IC[1])
        else:
            fb=0
            sb=IC
        IR="".join(str(data[fb][sb]))
        IC=IC+1
        loc=IR[2:]
        
        if IR[:2]=="GD":
            print("goto read at ",loc)
            SI=1
            MOS(loc)
            
        elif IR[:2]=="PD":
            print("goto write at ", loc)
            SI=2
            MOS(loc)
        
        elif IR[:2]=="LR":
            print("copying data to register")
            fb=int(int(loc)//10)
            sb=int(int(loc)%10)
            register=register+data[fb][sb]
            print("The value of M[",fb,"][",sb,"] stored in register R : ",register)
            
        elif IR[:2]=="CR":
            print("comparing data")
            fb=int(int(loc)//10)
            sb=int(int(loc)%10)
            if data[fb][sb]==register:
                print("Values of register and M[",fb,"][",sb,"] and register MATCH\n\n")
                flag=1
                
            else:
                flag=0
                print("Values of register and M[",fb,"][",sb,"] and register do not MATCH\n\n")
                
                
        elif IR[:2]=="BT":
            if flag==1:
                IC=IC+1
            else:
                pass
            
            
            
        elif IR[:2]=="SB":
            fb=int(int(loc)//10)
            sb=int(int(loc)%10)
            register=int(register)-int(data[fb][sb])
            print("The value of register R:",register+int(data[fb][sb]),
                  "after subtracting ",data[fb][sb],"is R: ",register)
            
        elif IR[:2]=="AD":
            fb=int(int(loc)//10)
            sb=int(int(loc)%10)
            register=int(register)+int(data[fb][sb])
            print("The value of register R:",register-int(data[fb][sb]),
                  "after adding ",data[fb][sb],"is R: ",register)
            
        elif IR[:2]=="DV":
            fb=int(int(loc)//10)
            sb=int(int(loc)%10)
            register=int(register)//int(data[fb][sb])
            print("The value of register R:",register*int(data[fb][sb]),
                  "after dividing",data[fb][sb],"is R: ",register)
            
        elif IR[:2]=="MB":
            fb=int(int(loc)//10)
            sb=int(int(loc)%10)
            register=int(register)*int(data[fb][sb])
            print("The value of register R:",register//int(data[fb][sb]),
                  "after multiplication ",data[fb][sb],"is R: ",register)
            
            
        elif IR[:2]=="SR":
            fb=int(int(loc)//10)
            sb=int(int(loc)%10)
            data[fb][sb]=register
            print("put the value of register at M[",fb,"][",sb,"]")
                
                
        elif IR[0] == "H":
            SI=3
            MOS(loc)
           
        

        
        
def load():
    global second_block
    global first_block
    global data
    global i
    global number_inst
    global register
    global AMJdata
    global total_data_count
    global jobid_check
    jobid=" "
    AMJinstructions=" "
    AMJdata=" "
    
    o=len(fp)
    temp=[]
    while(i<o-8):
        
        j=i+4
        while(i<j and fp[i]!="\n"):
            temp.append(fp[i])
            i=i+1
        tempstr="".join(temp) 
        temp=[]
        print(tempstr)
        
        
        if tempstr=="$AMJ":
            print("in AMJ\n")
            jobid="".join(fp[i:i+4])
            i=i+4
            AMJinstructions ="".join(fp[i+2:i+4])
            i=i+4
            AMJdata ="".join(fp[i+3:i+5])
            
            print("The job ID : ",jobid)
            print("The Number of instructions : ",AMJinstructions)
            print("The number of data cards : ",AMJdata)
            
            
            if(jobid_check==int(jobid)):
                pass
            else:
                print("Wrong job id written")
                exit()
            
            while(fp[i]!="\n"):
                i=i+1
                
                
        elif tempstr=="$DTA":
            execute()
            
        
            
        elif tempstr=="$END":
            i=i+4
            insert_newline()
    
            number_inst=0
            data = ''
            AMJdata=""
            data=[[],[],[],[],[],[],[],[],[],[],]
            for x in range(10):
                for y in range(10):
                    data[x].append([])  
            first_block=0
            second_block=0
            register=""
            total_data_count=0
            print("Flushing memory of previous job\n\n\n")
            jobid_check=jobid_check+1
            
            
            
            
            
        else :
            if second_block<10:
                data[first_block][second_block]=(tempstr) 
            else:
                first_block=first_block+1
                second_block=0
            second_block=second_block+1
            number_inst=number_inst+1
            if number_inst>int(AMJinstructions):
                print(number_inst,AMJinstructions)
                print("wrong number of instructions written\n\n")
                exit()
                
            if second_block==10:
                first_block=first_block+1
                second_block=0
        

        
        if(fp[i]== "\n"):
            i=i+1
            
    
    
    
    
def insert_newline():
    file2=open("python_output.txt",'a')
    file2.write("\n")
    
    
    
def display():
    fa=0
    sa=0
    for i in (data):
        for j in i:
            if j==[]:
                j=""
            print("M[",fa,"]:[",sa,"] = ",(j))
            if (sa==9):
                sa=-1
                fa=fa+1
            sa = sa+1
            
    print("\n\n")
            
    

file1 = open("C:\\Users\\aakas\\OneDrive\\Desktop\\java codes\\caos\\inputone.txt", 'r')
fp1=file1.read()
fp=list(fp1)
length=len(fp)

if (file1 == None ):
    print("File not found")

else:
    print("load")
    load()
file1.close()
#END
