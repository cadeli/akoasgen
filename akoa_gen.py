# -*- coding: utf-8 -*-
import pickle  #save
import ttk
import ast
import re
import tkFont
from Tkinter import *
from collections import namedtuple

UNIT_PX = 15


sprite1 =   {'name':'aa sprite 1', 'width' : '8', 'height': '8', 'animation_name' :'sprites_1', 'animation_frame_num':'0'}
sprite1_1 = {'name':'bb sprite 1', 'width' : '64', 'height': '8', 'animation_name' :'sprites_1', 'animation_frame_num':'1'}
sprite2 =   {'name':'cc sprite 2', 'width' : '8', 'height': '8', 'animation_name' :'sprites_2', 'animation_frame_num':'0'}
sprite3 =   {'name':'dd sprite 3', 'width' : '8', 'height': '8', 'animation_name' :'sprites_3', 'animation_frame_num':'0'}

sprites_list=(sprite1,sprite2,sprite3,sprite1_1)
current_sprite = sprite1

    
def draw_grid(canvas ):
    global current_sprite
    #print "drawgrid current_sprite = ", current_sprite
    offset_x =0
    offset_y = 0
    canvas.delete("all")
    for i in range (0,int(current_sprite["width"])) :
        for j in range (0,int(current_sprite["height"])) :
            x1 = i*UNIT_PX + offset_x
            y1 = j*UNIT_PX + offset_y
            x2 = x1+UNIT_PX
            y2 = y1+UNIT_PX
            canvas.create_rectangle(x1,y1,x2,y2,fill="white")
            
def draw_sprite(canvas):
    #print "drawsprite current_sprite = ", current_sprite
    global current_sprite
    for key, value in current_sprite.items() :
        if (re.match("^pix_", key)):
            #print "match ",key, value
            x=key.split('_')[1]
            y=key.split('_')[2]
            if (value==1):
                color="blue"
            draw_pix(canvas,int(x),int(y),color)

def draw_pix(canvas,x,y,color):
    #print "disp px: ",x,y, " col=",color
    offset_x=0
    offset_y = 0 
    x1=offset_x + UNIT_PX*x
    y1=offset_y + UNIT_PX*y
    canvas.create_rectangle(x1,y1,x1+UNIT_PX,y1+UNIT_PX, fill=color)

def on_grid_click(event):
    global current_sprite
    #print 'Got canvas click', event.x, event.y, event.widget
    grid_num =  0
    #current_akoa_form = akoa_form_dic[name,grid_num]
    offset_x=0
    offset_y = 0
    x = int((event.x - offset_x)/UNIT_PX)
    y = int((event.y - offset_y)/UNIT_PX)
   # print "on_grid_click current_sprite: ", current_sprite
    akoa_pix={"x":x,"y":y,"color":1}
    print "add pix ", akoa_pix
    key = 'pix_'+str(x)+'_'+str(y)
    if key in current_sprite:
        try:
            del current_sprite[key]
        except KeyError:
            pass
    else:
        current_sprite.update({key:1})
    #print "on_grid_click current_sprite: ", current_sprite
    draw_sprite_edit_canvas()

def clear_akoa_form( grid_num) :
    for x in range(0,AKOA_W):
        for y in range (0,AKOA_H):
            draw_pix(grids_canvas,x,y,"grey",grid_num)

def draw_akoa_form(akoa_form, grid_num,color) :                   
    for pix_id in akoa_form:
        #print "pix",pix_id, "=", akoa_form[pix_id]
        pix = akoa_form[pix_id]
        for attr in pix:
            draw_pix(grids_canvas,pix['x'],pix['y'],color,grid_num)

def save() :
    print "save "
     # ici le file selectetor (save as)
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
        draw_akoa_form(current_akoa_form,0,"blue")

def render() :
    print "render "
    print akoa_form_dic
    # ici le file selectetor (save as)

def new_sprite() :
    print "new sprite"


def draw_sprite_edit_canvas() :
    global current_sprite
    label_sprite_title.config(text=current_sprite["name"])
    draw_grid(grid_canvas)
    draw_sprite(grid_canvas);
    grid_canvas.update();
    label_sprite_title.update()
    sprite_edit_canvas.update()
  
def sprite_name_selected(event) :
    global sprites_list
    global current_sprite
    for el in sprites_list :
        if (el['name']== event.widget.get()) : 
            current_sprite = el
            #print "current_sprite is now: ", current_sprite
            draw_sprite_edit_canvas()
    
#print "name of sprite 1: ", sprites_list[0]["name"]
#print "name of sprite 1: ", sprite1["name"]
#print "name of sprite 1: ", current_sprite["name"]
#print "current_sprite: ", current_sprite

def maj_spritenames_list() :
    global sprites_list
    spritenames_list=list()
    for el in sprites_list :
        spritenames_list.append(el['name'])
    return spritenames_list

#########################################################
root= Tk()
customFont = tkFont.Font(family="Helvetica", size=24)
 
sprite_edit_canvas = Canvas(root, bg="white")
label_sprite_title = Label(sprite_edit_canvas,text="", width=64, relief = GROOVE, fg="red",font=customFont)
label_sprite_title.pack(side=TOP)
grid_canvas = Canvas(sprite_edit_canvas,   relief = GROOVE, bg="white")
grid_canvas.bind('<ButtonPress-1>', on_grid_click)    
grid_canvas.pack(fill="both", expand=True)
draw_sprite_edit_canvas()


#spritetoolbar
sprite_tool_bar_canvas = Canvas(root,  height=512, relief = GROOVE)
button_new_sprite = Button(sprite_tool_bar_canvas,text="new anim",command=new_sprite, width=8)
button_new_sprite.grid(row=1,column=0, padx =5, pady =5)
button_new_sprite = Button(sprite_tool_bar_canvas,text="delete anim",command=new_sprite, width=8)
button_new_sprite.grid(row=1,column=1, padx =5, pady =5)

spritenames_list = maj_spritenames_list()
combo_sprite_list = ttk.Combobox(sprite_tool_bar_canvas,values = spritenames_list, width=32)
combo_sprite_list.grid(row=0,column=0, padx =5, pady =5,columnspan=2)
combo_sprite_list.set(spritenames_list[0])
combo_sprite_list.bind("<<ComboboxSelected>>", sprite_name_selected)

#maintoolbar
main_tool_bar_canvas = Canvas(root, bg="grey", width=512, height=512, relief = GROOVE)
button_save = Button(main_tool_bar_canvas,text="Save",command=save, width=3)
button_save.grid(row=0,column=0, padx =5, pady =0)
button_read = Button(main_tool_bar_canvas,text="Read",command=read, width=3)
button_read.grid(row=0,column=1, padx =5, pady =0)
button_render = Button(main_tool_bar_canvas,text="Render",command=render, width=3)
button_render.grid(row=1,column=0, padx =5, pady =0)
button_exit = Button(main_tool_bar_canvas,text="Sortir",command=root.destroy, width=3)
button_exit.grid(row=2,column=0, padx =5, pady =0)

sprite_tool_bar_canvas.pack(side=TOP)
sprite_edit_canvas.pack(fill="both", expand=True) #Affiche le canevas
main_tool_bar_canvas.pack(side=LEFT)



root.mainloop()
