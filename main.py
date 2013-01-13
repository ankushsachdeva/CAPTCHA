from Tkinter import *
import tkFileDialog
import tkMessageBox
from PIL import Image,ImageTk
import math

def identify(max):			#to match the current character info with the database
    min=999999
    fread=open("train.txt","r")
    while(1):
        sum=0
        str=fread.readline().split()
        if(str==[]):
            
            return store,min
        #print str
        for i in range(1,19):
            sum=sum+abs(max[i-1]-float(str[i]))
       # if(str[0]=='G'):print "g=",(36-sum)*100.0/36,"%"
        if(sum<min):
            min=sum
            store=str[0]


            

def symline(linesavg):		#to find the symetry line
    min=999999
    
    for i in range(18):
        sod=0
        j=i+1
        while(j-i!=18):
            if(j>35):
                sod+=abs(linesavg[j-36]-linesavg[2*i-j])
            else:
                sod+=abs(linesavg[j]-linesavg[2*i-j])
            j+=1
        #print sod
        if(sod<min):
            min=sod
            
            store=i
    return store
                
        
def inframe(x,y):			#to prevent segmentation fault
    if(x>=0 and x<200 and y >=0 and y<40):
        return 1
    return 0

def drawline(origin,previ,latei,out):	#to draw a line
    linesavg=[0]*36
    linesmax=[0]*36
    
    pixd=out.load()
    for angle in range(0,360,10):
        x=origin[0]
        y=origin[1]
        count=0
        
        
        m=math.tan(math.radians(angle))
        while(x>=previ and x<=latei and inframe(x,y)==1):
            
            if(pixd[x,y]==0):
                linesavg[(angle/10)]+=(x-origin[0])*(x-origin[0])+(y-origin[1])*(y-origin[1])
                count+=1
                if((x-origin[0])*(x-origin[0])+(y-origin[1])*(y-origin[1])>linesmax[angle/10]):linesmax[angle/10]=(x-origin[0])*(x-origin[0])+(y-origin[1])*(y-origin[1])
            pixd[x,y]=120
            if(m>=0 and angle<45):
                x+=1
                if((x-origin[0])*m>1+y-origin[1]):
                    y+=1
            if(angle>45 and angle<=90):
                y+=1
                if((y-origin[1])>(1+x-origin[0])*m):
                    x+=1
            if(angle>90 and angle<135):
                y+=1
                if((y-origin[1])>(1-x+origin[0])*-m):
                    x-=1
            if(angle>135 and angle<=180):
                x-=1
                if((-x+origin[0])*-m>1+y-origin[1]):
                    y+=1
            if(angle>180 and angle<225):
                x-=1
                if((-x+origin[0])*m>1-y+origin[1]):
                    y-=1
            if(angle>225 and angle<=270):
                y-=1
                if((-y+origin[1])>(1-x+origin[0])*m):
                    x-=1
            if(angle>270 and angle<315):
                y-=1
                if((-y+origin[1])>(1+x-origin[0])*-m):
                    x+=1
            if(angle>315 and angle<360):
                x+=1
                if((x-origin[0])*-m>1-y+origin[1]):
                    y-=1
        if(count!=0):linesavg[(angle/10)]/=count*1.0
    out.save("testing.gif")
    #print linesmax
    return (linesavg,linesmax)
                
                
                
        
        


def findsize(i,f,com,pix):		#to find the distance between COM and the farthest point
    maxsq=0
    for i in range(i,f+1):
        for j in range(40):
            if(pix[i,j]==0):
                if((i-com[0])*(i-com[0])+(j-com[1])*(j-com[1])>maxsq):
                    maxsq=(i-com[0])*(i-com[0])+(j-com[1])*(j-com[1])
    return maxsq
    
def findcom(i,f,pix):			#to find COM
    
    xsum=0
    ysum=0
    count=0
    for i in range(i,f):
        for j in range(40):
            if(pix[i,j]==0):
                xsum=xsum+i
                ysum=ysum+j
                count=count+1
    return (int(round(xsum/count)),int(round(ysum/count)))


def edge(tup,pixi):			#to check if a given pixel is edge of a character
    for l in (1,0,-1):
        for m in(1,0,-1):
            if((l==0 and m==0)):continue
            if((tup[0]+l==200)or(tup[0]+l==-1)or(tup[1]+m==-1)or(tup[1]+m)==40):
                return 1
            if(pixi[tup[0]+l,tup[1]+m][0]>125):
                return 1
    return 0
    
def dialog():				#action of the browse button->open the file dialog box and then show that image at the top
    global filename
    filename=tkFileDialog.askopenfilename(filetypes=[("Image","*.jpg")])
    entryWidget.delete(0,END)
    entryWidget.insert(0,filename)
    
    global photo
    global image
    global imagelabel
    image=Image.open(filename)
    photo=ImageTk.PhotoImage(image)
    imagelabel.pack_forget()
    imagelabel=Label(outputframe,image=photo)
    imagelabel.pack(side=TOP)
    
   
def convertimage(im,noise):		#to convert background into white and characters to black
    str=im.getpixel((0,0))
    pixi=im.load()
    
    for i in range(200):
        for j in range(40):
            if (((abs(pixi[i,j][0]-str[0])<noise)and(abs(pixi[i,j][1]-str[1])<noise)and(abs(pixi[i,j][2]-str[2])<noise))):
                pixi[i,j]=(255,255,255)
            else:
                pixi[i,j]=(0,0,0)
    return pixi

def trainscreen():			# to get the new image in training GUI screen
    global image,templabel
    answerframe.pack_forget()
    trainframe.pack(pady=20)
    templabel.pack_forget()
    im=Image.open(entryWidget.get().strip())
    pixi=convertimage(im,35)
  
    out=Image.new("L",(201,40),251)
    pix=out.load()
    for i in range (200):
        for j in range(40):
            if(pixi[i,j][0]<150 and edge((i,j),pixi)==1):
               pix[i,j]=0
    out.save("temp.gif")
    out=Image.open("temp.gif")
    image=ImageTk.PhotoImage(out)
    templabel=Label(outputframe,image=image)
    templabel.pack()
    
    
    
def training():		#training GUI screen
    
    inp=traininput.get()
    inp=inp.upper()
    count=0
    im=Image.open(entryWidget.get().strip())
    pixi=convertimage(im,35)
    fout=open("train.txt","a")
    out=Image.new("L",(201,40),251)
    pix=out.load()
    for i in range (200):
        for j in range(40):
            if(pixi[i,j][0]<150 and edge((i,j),pixi)==1):
               pix[i,j]=0
    checker=0

    previ=0
    for i in range(201):
        for j in range(20,40)+range(0,20):
            if(pix[i,j]==0):
                checker=1
                break
        if(j==19and checker==1):
            com=findcom(previ,i,pix)
        
            lines=drawline(com,previ,i,out)
            avg=lines[0]
            max=lines[1]
            smax=symline(max)
            size=findsize(previ,i,com,pix)
            for l in range(18):
                max[l]=(max[l]+max[18+l])*1.0/size
            max=max[smax:18]+max[:smax]
            answer=identify(max)
            print answer
            if((answer[1]>1.8 or answer[0]<>inp[count])and inp[count]<>" "):
                print inp[count]
                fout.write(inp[count]+" ")
                fout.writelines(["%s "%item for item in max])
                fout.write("\n")
            
            count+=1
        
        
            pix[com[0],com[1]]=100
            previ=i
            checker=0

    tkMessageBox.showinfo("Update Successful","train.txt updated!!")    
    fout.close()   
            
            
    
    
def main():		#main decoding function
    global templabel
    templabel.pack_forget()
    trainframe.pack_forget()	#to hide the training screen if its open
    answerframe.pack(pady=20)
    im=Image.open(entryWidget.get().strip())	#to get the image name from browse test field
    pixi=convertimage(im,35)			#convert image to black n white
    
    out=Image.new("L",(201,40),251)
    pix=out.load()
    t=1

    for i in range (200):
        for j in range(40):
            if(pixi[i,j][0]<150 and edge((i,j),pixi)==1):	#extract the edge
               pix[i,j]=0
    checker=0

    previ=0

    for i in range(201):					#to extract each character one by one and decode
    
        for j in range(20,40)+range(0,20):
            if(pix[i,j]==0):
                checker=1
                break
        if(j==19and checker==1 ):				#this will happen only if a complete vertical row is white and
								# there was at least 1 black pixel aftre the ending of the previous character
           
            com=findcom(previ,i,pix)
            #print com
            size=findsize(previ,i,com,pix)
            lines=drawline(com,previ,i,out)
            avg=lines[0]					#avg is the list with average distances of the pixels from the centre along a line
								#avg was not giving accurate results and is not used in the identification

            max=lines[1]					#max distances of a pixels from centre along ecah line					
            smax=symline(max)					#ray which has max symmetry about it
            for l in range(18):
                max[l]=(max[l]+max[18+l])*1.0/size		#we had 36 rays ,we store it as 18 lines 
            max=max[smax:18]+max[:smax]
            
            answer=identify(max)
                                
                
            text[t].set(answer[0])				
            textper[t].set(answer[1])				
            
            t+=1
            
            pix[com[0],com[1]]=100
            previ=i
            checker=0
    if(t<6):
        tkMessageBox.showinfo("Error","characters not spaced properly")
        
filename=" "					#GUI code
image=None
root = Tk()
root.title("IITK CAPTCHA Decoder")
root["padx"] = 20
root["pady"] = 20
root.geometry('680x450+200+200')
inputframe=Frame(root,relief=GROOVE,borderwidth=2,pady=5)
inputframe.pack(side=BOTTOM,fill=X)
    
    #Create a Label in textFrame
Label(inputframe,text="Captcha file(in jpg ONLY)").pack(side=LEFT)

    # Create an Entry Widget in textFrame
entryWidget = Entry(inputframe)
#entryWidget["width"] = 50
entryWidget.pack(side=LEFT,padx=20)


Button(inputframe,text="Browse",command=dialog).pack(side=LEFT)


submit= Button(inputframe, text="Decode", command=main)
train=Button(inputframe,text="Train",command=trainscreen)

submit.pack(side=RIGHT,padx=30)
train.pack(side=RIGHT)

outputframe=Frame(root,relief=GROOVE,borderwidth=2,pady=5)
outputframe.pack(side=TOP,fill=X)
photo=ImageTk.PhotoImage(Image.new("L",(200,40),251))

Label(outputframe,text="CAPTCHA image").pack()
imagelabel=Label(outputframe,image=photo)
imagelabel.pack(side=TOP)
templabel=Label(outputframe,image=photo)
answerframe=Frame(root,relief=GROOVE,borderwidth=2)
answerframe.pack(pady=20)
trainframe=Frame(root,relief=GROOVE,borderwidth=2)
traininput=Entry(trainframe)
traininput.pack(pady=5)
trainbutton=Button(trainframe,text="Train it!!",command=training)
trainbutton.pack(pady=5)
Label(trainframe,text="""Train only if a character is clearly visible in the new image
generated above but it is not being recognized correctly .To
leave a charcter untrained put a space instead""").pack()

char=[0]*8
charper=[0]*8
text=[0]*8
textper=[0]*8
for t in range(8):
    text[t]=StringVar()
    text[t].set(" ")
    textper[t]=StringVar()
    #textper[t].set("87%")
    char[t]=Label(answerframe,textvariable=text[t],font=("Helvetica", 16))
    char[t].pack(side=LEFT,padx=9)
    charper[t]=Label(answerframe,textvariable=textper[t])

#fLabel(answerframe,textvariable=textper[t]).pack(side=BOTTOM)





root.mainloop()
