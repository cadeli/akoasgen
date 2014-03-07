# -*- coding: utf-8 -*-
import pickle  #save
from Tkinter import *
#test
UNIT_PX = 15
AKOA_H = 8
AKOA_W = 8

def getOffsetsFrumGridNum(grid_num):
    offset_x = AKOA_W + (grid_num*UNIT_PX*(AKOA_W+2))
    offset_y = AKOA_H     
    return (offset_x,offset_y)
    
def drawGrid(canvas,grid_num):
    offset_x,offset_y = getOffsetsFrumGridNum(grid_num) 
    for i in range (0,AKOA_W) :
        for j in range (0,AKOA_H) :
            x1 = i*UNIT_PX + offset_x
            y1 = j*UNIT_PX + offset_y
            x2 = x1+UNIT_PX
            y2 = y1+UNIT_PX
            canvas.create_rectangle(x1,y1,x2,y2)

def drawPix(canvas,x,y,color,grid_num):
    #print("disp px: ",x,y)
    offset_x,offset_y = getOffsetsFrumGridNum(grid_num) 
    x1=offset_x + UNIT_PX*x
    y1=offset_y + UNIT_PX*y
    canvas.create_rectangle(x1,y1,x1+UNIT_PX,y1+UNIT_PX, fill=color)


#def drawBg(canvas) :  
    #canvas.create_line(0,0,499,499) #Dessine une ligne en diagonale
    #canvas.create_rectangle( 0,0,UNIT_PX*10,UNIT_PX*10, fill="white")

def onCanvasClick(event):
    #print 'Got canvas click', event.x, event.y, event.widget
    grid_num =   int((event.x-UNIT_PX) /(UNIT_PX*(AKOA_W+2)))
    current_akoa_form = akoa_form_dic[name,grid_num]
    offset_x,offset_y = getOffsetsFrumGridNum(grid_num) 
    x = int((event.x - offset_x)/UNIT_PX)
    y = int((event.y - offset_y)/UNIT_PX)
    akoa_pix={"x":x,"y":y,"color":1}
    akoa_pix_val=x,y
    if  akoa_pix_val in current_akoa_form :
         current_akoa_form.pop(akoa_pix_val,0)
         clearAkoaForm(grid_num)
    else :
        current_akoa_form[x,y]=akoa_pix
    drawAkoaForm(current_akoa_form,grid_num,"blue")


def clearAkoaForm( grid_num) :
    for x in range(0,AKOA_W):
        for y in range (0,AKOA_H):
            drawPix(gridsCanvas,x,y,"grey",grid_num)

def drawAkoaForm(akoa_form, grid_num,color) :                   
    for pix_id in akoa_form:
        #print "pix",pix_id, "=", akoa_form[pix_id]
        pix = akoa_form[pix_id]
        for attr in pix:
            drawPix(gridsCanvas,pix['x'],pix['y'],color,grid_num)

def save() :
    print "save "
    with open('akoa_as_list.txt','wb') as out_file:
        my_pickler = pickle.Pickler(out_file)
        my_pickler.dump(current_akoa_form)
        out_file.close()    

def read() :
    print "read "
    with open('akoa_as_list.txt','rb') as in_file:
        my_pickler = pickle.Unpickler(in_file)
        current_akoa_form = my_pickler.load()
        in_file.close()
        drawAkoaForm(current_akoa_form,0,"blue")

def render() :
    print "render "
    print akoa_form_dic
    for grid_num in range (1,8) :
        drawAkoaForm(akoa_form_dic[name,grid_num-1],grid_num,"red")
        drawAkoaForm(akoa_form_dic[name,grid_num],grid_num,"blue")

def new_sprite() :
    print "new sprite"

#akoa_pix1={"x":0,"y":0,"color":1}
#akoa_pix2={"x":1,"y":1,"color":1}
#akoa_pix3={"x":2,"y":1,"color":1}
#akoa_pix4={"x":1,"y":2,"color":1}   

#akoa_form1 = {"1":akoa_pix1,"2":akoa_pix2,"3":akoa_pix2}
#print "akoaform_1", akoa_form1
current_akoa_form = {}
    
root= Tk()
 
gridsCanvas = Canvas(root, bg="white", width=1224, height=512)
gridsCanvas.bind('<ButtonPress-1>', onCanvasClick)                
#drawBg(canvas)

akoa_form_dic = {}
name="basicAkoa"
for grid_num in range (0,8) :
    akoa_form = {}
    akoa_form_dic[name,grid_num]=akoa_form
    drawGrid(gridsCanvas,grid_num)
#drawAkoaForm(akoa_form1)


spriteToolBarCanvas = Canvas(root, bg="red",  height=512, relief = GROOVE)
button_newSprite = Button(spriteToolBarCanvas,text="new sprite",command=new_sprite, width=8)
button_newSprite.grid(row=1,column=0, padx =5, pady =5)
button_newSprite = Button(spriteToolBarCanvas,text="delete sprite",command=new_sprite, width=8)
button_newSprite.grid(row=1,column=1, padx =5, pady =5)
spin_spriteList = Spinbox(spriteToolBarCanvas,from_=0,to=7)
spin_spriteList.grid(row=0,column=0, padx =5, pady =5,columnspan=2)


mainToolBarCanvas = Canvas(root, bg="grey", width=512, height=512, relief = GROOVE)
button_save = Button(mainToolBarCanvas,text="Save",command=save, width=3)
button_save.grid(row=0,column=0, padx =5, pady =0)
button_read = Button(mainToolBarCanvas,text="Read",command=read, width=3)
button_read.grid(row=0,column=1, padx =5, pady =0)
button_render = Button(mainToolBarCanvas,text="Render",command=render, width=3)
button_render.grid(row=1,column=0, padx =5, pady =0)
bouton_sortir = Button(mainToolBarCanvas,text="Sortir",command=root.destroy, width=3)
bouton_sortir.grid(row=2,column=0, padx =5, pady =0)



spriteToolBarCanvas.pack(side=TOP)
gridsCanvas.pack(fill="both", expand=True) #Affiche le canevas
mainToolBarCanvas.pack(side=LEFT)



root.mainloop()
