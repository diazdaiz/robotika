# Basic OBJ file viewer. needs objloader from:
#  http://www.pygame.org/wiki/OBJFileLoader
# LMB + move: rotate
# RMB + move: pan
# Scroll wheel: zoom in/out
import sys, pygame
from pygame.locals import *
from pygame.constants import *
from OpenGL.GL import *
from OpenGL.GLU import *
import Fungsi as f
import Class as c

# IMPORT OBJECT LOADER
from objloader import *

# IMPORT TKINTER
from tkinter import *

width=800
height=600
pygame.init()
viewport = (width,height)
hx = viewport[0]/2
hy = viewport[1]/2
srf = pygame.display.set_mode(viewport, OPENGL | DOUBLEBUF)
pygame.display.set_caption("simulator")

glLightfv(GL_LIGHT0, GL_POSITION,  (-40, 200, 100, 0.0))
glLightfv(GL_LIGHT0, GL_AMBIENT, (0.2, 0.2, 0.2, 1.0))
glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.5, 0.5, 0.5, 1.0))
glEnable(GL_LIGHT0)
glEnable(GL_LIGHTING)
glEnable(GL_COLOR_MATERIAL)
glEnable(GL_DEPTH_TEST)
glShadeModel(GL_SMOOTH)           # most obj files expect to be smooth-shaded

# Load Data
c.Part.load_data()  

# LOAD OBJECT AFTER PYGAME INIT
part=[]
for i in range(0,27):
    '''pilih, kalau 1 diantara 3, opt->optimize, jadi lebih ga lag kalau milih opt. opt_2 lebih ga lag lagi, 
    cuman cuma kotak-kotak aja. kalau yg ga di opt biasanya nunggu sekitar 1 menitan baru kebuka'''
    part.append(OBJ("part_"+str(i)+".obj", swapyz=True))
    #part.append(OBJ("part_"+str(i)+"_opt.obj", swapyz=True))
    #part.append(OBJ("part_"+str(i)+"_opt_2.obj", swapyz=True))

clock = pygame.time.Clock()

glMatrixMode(GL_PROJECTION)
glLoadIdentity()
width, height = viewport
gluPerspective(90.0, width/float(height), 1, 1000.0)
glEnable(GL_DEPTH_TEST)
glMatrixMode(GL_MODELVIEW)

rx, ry = (0,0)
tx, ty = (2000,-6000) #set initial traslation for x and y
zpos = 500 #set initial z position (translation z)
rotate = move = False

rotasi_servo=[]
for i in range(27):
    rotasi_servo.append(0)

#tkinter function
def slide_tx(val):
    global tx
    tx=float(val)
    draw()
    
def slide_ty(val):
    global ty
    ty=float(val)
    draw()
    
def slide_scale(val):
    global zpos
    zpos=float(val)
    draw()

def slide_rx(val):
    global rx
    rx=float(val)
    draw()
    
def slide_servo(val):
    global rotasi_servo
    no_servo=int(entry_no_servo.get())
    rotasi_servo[no_servo]=float(val)
    draw()

#transformation function
def transformation_0(kaki, pe, di, ur): #pentransformasi, ditrasformasi, urutan
    glTranslate(c.part[kaki][pe].koordinat_sumbu_rotasi_servo.elemen[0][0]+tx/20, c.part[kaki][pe].koordinat_sumbu_rotasi_servo.elemen[1][0]+ty/20, c.part[kaki][pe].koordinat_sumbu_rotasi_servo.elemen[2][0]-zpos)
    if(pe==0 or pe==3 or pe==4 or pe==7 or pe==8 or pe==16 or pe==17 or pe==20 or pe==21 or pe==22 or pe==23):
        glRotatef(rotasi_servo[pe],1,0,0)
    elif(pe==2 or pe==9 or pe==10 or pe==11 or pe==12 or pe==13 or pe==14 or pe==15):
        glRotatef(rotasi_servo[pe],0,1,0)
    elif(pe==1 or pe==5 or pe==6 or pe==18 or pe==19 or pe==24 or pe==25 or pe==26):
        glRotatef(rotasi_servo[pe],0,0,1)
    glTranslate(-c.part[kaki][pe].koordinat_sumbu_rotasi_servo.elemen[0][0]-tx/20, -c.part[kaki][pe].koordinat_sumbu_rotasi_servo.elemen[1][0]-ty/20, -c.part[kaki][pe].koordinat_sumbu_rotasi_servo.elemen[2][0]+zpos)
    if(pe!=di):
        transformation_0(kaki,c.part[kaki][di].urutan_transformasi[ur+1],di,ur+1)

def transformation():
    for i in range(27):
        glLoadIdentity() #reset matix to identity matrix
        transformation_0(0,25,i,0)
        glTranslate(tx/20., ty/20., - zpos)
        glCallList(part[i].gl_list) #set part i to the transformed position in opengl
    
#draw to opengl
def draw():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    transformation()
    # render object
    pygame.display.flip()

#add gui to tkinter
root=Tk()
root.title("Simulator")
root.geometry("300x600")

frame_controller=Frame(root, width=300, height=600)
frame_controller.grid(row=0, column=0)

label_no_servo=Label(frame_controller, text="no servo:")
label_no_servo.grid(row=0,column=0)

entryText = StringVar()
entry_no_servo=Entry(frame_controller, textvariable=entryText)
entry_no_servo.grid(row=0, column=1)
entryText.set("26")

slider_rservo=Scale(frame_controller, orient=HORIZONTAL, command=slide_servo, length=200, from_=-180, to=180)
slider_rservo.grid(row=1,column=1)

label_tx=Label(frame_controller, text="x:")
label_tx.grid(row=2, column=0)

slider_tx=Scale(frame_controller, orient=HORIZONTAL, command=slide_tx, length=200, from_=-3000, to=7000)
slider_tx.grid(row=2, column=1)
slider_tx.set(2000)

label_tx=Label(frame_controller, text="y:")
label_tx.grid(row=3, column=0)

slider_ty=Scale(frame_controller, command=slide_ty, length=200, from_=-10000, to=0)
slider_ty.grid(row=3, column=1)
slider_ty.set(-6000)

label_scale=Label(frame_controller, text="scale:")
label_scale.grid(row=4, column=0)

slider_scale=Scale(frame_controller, orient=HORIZONTAL, command=slide_scale, length=200, from_=100, to=500)
slider_scale.grid(row=4, column=1)
slider_scale.set(500)

draw()

#looping pygame with pygame clock
while 1:
    clock.tick(30)
    root.update() #update tkinter inside pygame loop