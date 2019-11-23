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
import pdb
import math
import numpy
import tinyik

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
part=[[],[]]
for i in range(28):
    '''pilih 1 diantara 3, opt->optimize, jadi lebih ga lag kalau milih opt. opt_2 lebih ga lag lagi, 
    cuman cuma kotak-kotak aja. kalau yg ga di opt biasanya nunggu sekitar 1 menitan baru kebuka'''
    #part[0].append(OBJ("part_"+str(i)+"_0.obj", swapyz=True))
    part[0].append(OBJ("part_"+str(i)+"_opt_1_0.obj", swapyz=True))
    #part[0].append(OBJ("part_"+str(i)+"_opt_2_0.obj", swapyz=True))
    
    #part[1].append(OBJ("part_"+str(i)+"_1.obj", swapyz=True))
    part[1].append(OBJ("part_"+str(i)+"_opt_1_1.obj", swapyz=True))
    #part[1].append(OBJ("part_"+str(i)+"_opt_2_1.obj", swapyz=True))
    
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
napak=False
step_time=0
'''
for i in range(150):
    mtemp_1=[]
    for j in range(20):
        mtemp_1.append(0)
    step_time.append(mtemp_1)
'''
page_step_rotasi=[]
rotasi_servo=[]
for i in range(27):
    rotasi_servo.append(0)
    
for i in range(150):
    mtemp_2=[]
    for j in range(20):
        mtemp_1=[]
        for k in range(28):
            mtemp_1.append(0)
        mtemp_2.append(mtemp_1)
    page_step_rotasi.append(mtemp_2)

#tkinter function
def slide_tx(val):
    global tx
    tx=float(val)
    
def slide_ty(val):
    global ty
    ty=float(val)
    
def slide_scale(val):
    global zpos
    zpos=float(val)

def slide_rx(val):
    global rx
    rx=float(val)
    
def update_sudut_servo():
    for i in range(27):
        rotasi_servo[i]=page_step_rotasi[int(entry_page.get())][int(entry_step.get())][i]
    
    c.part[0][0].rotasi=f.matriks_rotasi(0, rotasi_servo[0])
    c.part[0][1].rotasi=f.matriks_rotasi(2, rotasi_servo[1])
    c.part[0][2].rotasi=f.matriks_rotasi(1, rotasi_servo[2])
    c.part[0][3].rotasi=f.matriks_rotasi(0, rotasi_servo[3]-90)
    c.part[0][4].rotasi=f.matriks_rotasi(0, rotasi_servo[4]-90)
    c.part[0][5].rotasi=f.matriks_rotasi(2, rotasi_servo[5])
    c.part[0][6].rotasi=f.matriks_rotasi(2, rotasi_servo[6])
    c.part[0][7].rotasi=f.matriks_rotasi(0, rotasi_servo[7]+90)
    c.part[0][8].rotasi=f.matriks_rotasi(0, rotasi_servo[8]+90)
    c.part[0][9].rotasi=f.matriks_rotasi(1, rotasi_servo[9])
    c.part[0][10].rotasi=f.matriks_rotasi(1, rotasi_servo[10])
    c.part[0][11].rotasi=f.matriks_rotasi(1, rotasi_servo[11])
    c.part[0][12].rotasi=f.matriks_rotasi(1, rotasi_servo[12])
    c.part[0][13].rotasi=f.matriks_rotasi(1, rotasi_servo[13])
    c.part[0][14].rotasi=f.matriks_rotasi(1, rotasi_servo[14])
    c.part[0][15].rotasi=f.matriks_rotasi(1, rotasi_servo[15])
    c.part[0][16].rotasi=f.matriks_rotasi(0, rotasi_servo[16])
    c.part[0][17].rotasi=f.matriks_rotasi(0, rotasi_servo[17])
    c.part[0][18].rotasi=f.matriks_rotasi(2, rotasi_servo[18])
    c.part[0][19].rotasi=f.matriks_rotasi(2, rotasi_servo[19])
    c.part[0][20].rotasi=f.matriks_rotasi(0, rotasi_servo[20])
    c.part[0][21].rotasi=f.matriks_rotasi(0, rotasi_servo[21])
    c.part[0][22].rotasi=f.matriks_rotasi(0, rotasi_servo[22])
    c.part[0][23].rotasi=f.matriks_rotasi(0, rotasi_servo[23])
    c.part[0][24].rotasi=f.matriks_rotasi(2, rotasi_servo[24])
    c.part[0][25].rotasi=f.matriks_rotasi(2, rotasi_servo[25])
    c.part[0][26].rotasi=f.matriks_rotasi(2, rotasi_servo[26])
    c.part[0][27].rotasi=f.matriks_rotasi(0, 0)
    c.part[0][28].rotasi=f.matriks_rotasi(0, 0)
    c.part[0][29].rotasi=f.matriks_rotasi(0, 0)
    c.part[0][30].rotasi=f.matriks_rotasi(0, 0)
    c.part[0][31].rotasi=f.matriks_rotasi(0, 0)
    
    c.part[1][0].rotasi=f.matriks_rotasi(0, rotasi_servo[0])
    c.part[1][1].rotasi=f.matriks_rotasi(2, rotasi_servo[1])
    c.part[1][2].rotasi=f.matriks_rotasi(1, rotasi_servo[2])
    c.part[1][3].rotasi=f.matriks_rotasi(0, rotasi_servo[3])
    c.part[1][4].rotasi=f.matriks_rotasi(0, rotasi_servo[4]-90)
    c.part[1][5].rotasi=f.matriks_rotasi(2, rotasi_servo[5]-90)
    c.part[1][6].rotasi=f.matriks_rotasi(2, rotasi_servo[6])
    c.part[1][7].rotasi=f.matriks_rotasi(0, rotasi_servo[7])
    c.part[1][8].rotasi=f.matriks_rotasi(0, rotasi_servo[8]+90)
    c.part[1][9].rotasi=f.matriks_rotasi(1, rotasi_servo[9]+90)
    c.part[1][10].rotasi=f.matriks_rotasi(1, rotasi_servo[10])
    c.part[1][11].rotasi=f.matriks_rotasi(1, rotasi_servo[11])
    c.part[1][12].rotasi=f.matriks_rotasi(1, rotasi_servo[12])
    c.part[1][13].rotasi=f.matriks_rotasi(1, rotasi_servo[13])
    c.part[1][14].rotasi=f.matriks_rotasi(1, -rotasi_servo[14])
    c.part[1][15].rotasi=f.matriks_rotasi(1, -rotasi_servo[15])
    c.part[1][16].rotasi=f.matriks_rotasi(0, -rotasi_servo[16])
    c.part[1][17].rotasi=f.matriks_rotasi(0, -rotasi_servo[17])
    c.part[1][18].rotasi=f.matriks_rotasi(2, -rotasi_servo[18])
    c.part[1][19].rotasi=f.matriks_rotasi(2, -rotasi_servo[19])
    c.part[1][20].rotasi=f.matriks_rotasi(0, -rotasi_servo[20])
    c.part[1][21].rotasi=f.matriks_rotasi(0, -rotasi_servo[21])
    c.part[1][22].rotasi=f.matriks_rotasi(0, -rotasi_servo[22])
    c.part[1][23].rotasi=f.matriks_rotasi(0, -rotasi_servo[23])
    c.part[1][24].rotasi=f.matriks_rotasi(2, -rotasi_servo[24])
    c.part[1][25].rotasi=f.matriks_rotasi(2, -rotasi_servo[25])
    c.part[1][26].rotasi=f.matriks_rotasi(2, rotasi_servo[26])
    c.part[1][27].rotasi=f.matriks_rotasi(0, 0)
    c.part[1][28].rotasi=f.matriks_rotasi(0, 0)
    c.part[1][29].rotasi=f.matriks_rotasi(0, 0)
    c.part[1][30].rotasi=f.matriks_rotasi(0, 0)
    c.part[1][31].rotasi=f.matriks_rotasi(0, 0)
    
def slide_servo(val):
    global napak
    global rotasi_servo
    rotasi_servo[int(entry_no_servo.get())]=int(val)
    page_step_rotasi[int(entry_page.get())][int(entry_step.get())][int(entry_no_servo.get())]=rotasi_servo[int(entry_no_servo.get())]
    
    
def update_step_time():
    global step_time
    step_time=page_step_rotasi[int(entry_page.get())][int(entry_step.get())][27]
    #page_step_rotasi[int(entry_page.get())][int(entry_step.get())][27]=entry_step_time.get()
    #step_time=page_step_rotasi[int(entry_page.get())][int(entry_step.get())][27]

def slide_step_time(val):
    step_time=int(val)
    page_step_rotasi[int(entry_page.get())][int(entry_step.get())][27]=step_time

def save_all():
    print("save") #liat format page
    print("load_all_page")

#transformation function
def transformation_0(kaki, pe, di, ur): #pentransformasi, ditrasformasi, urutan
    glTranslate(c.part[kaki][pe].koordinat_sumbu_rotasi_servo.elemen[0][0]+tx/20, c.part[kaki][pe].koordinat_sumbu_rotasi_servo.elemen[1][0]+ty/20, c.part[kaki][pe].koordinat_sumbu_rotasi_servo.elemen[2][0]-zpos)
    if(pe==0 or pe==3 or pe==4 or pe==7 or pe==8 or pe==16 or pe==17 or pe==20 or pe==21 or pe==22 or pe==23):
        if(kaki==1 and (pe==16 or pe==17 or pe==20 or pe==21 or pe==22 or pe==23)):
            glRotatef(-rotasi_servo[pe],1,0,0)
        else:
            if(pe==3 or pe==4):
                glRotatef(rotasi_servo[pe]-90,1,0,0)
            elif(pe==7 or pe==8):
                glRotatef(rotasi_servo[pe]+90,1,0,0)
            else:
                glRotatef(rotasi_servo[pe],1,0,0)
    elif(pe==2 or pe==9 or pe==10 or pe==11 or pe==12 or pe==13 or pe==14 or pe==15):
        if(kaki==1 and (pe==14 or pe==15)):
            glRotatef(-rotasi_servo[pe],0,1,0)
        else:
            glRotatef(rotasi_servo[pe],0,1,0)
    elif(pe==1 or pe==5 or pe==6 or pe==18 or pe==19 or pe==24 or pe==25 or pe==26):
        if(kaki==1 and (pe==18 or pe==19 or pe==24 or pe==25)):
            glRotatef(-rotasi_servo[pe],0,0,1)
        else:
            glRotatef(rotasi_servo[pe],0,0,1)
    glTranslate(-c.part[kaki][pe].koordinat_sumbu_rotasi_servo.elemen[0][0]-tx/20, -c.part[kaki][pe].koordinat_sumbu_rotasi_servo.elemen[1][0]-ty/20, -c.part[kaki][pe].koordinat_sumbu_rotasi_servo.elemen[2][0]+zpos)
    if(pe!=di):
        transformation_0(kaki,c.part[kaki][di].urutan_transformasi[ur+1],di,ur+1)

def transformation():
    for i in range(28):
        glLoadIdentity() #reset matix to identity matrix
        if(radio_button_kaki_napak_variable.get()==0):
            if(i==27):
                transformation_0(0,27,i,0)
            else:
                transformation_0(0,25,i,0)
        else:
            if(i==27):
                transformation_0(1,27,i,0)
            else:
                transformation_0(1,24,i,0)
        glTranslate(tx/20., ty/20., - zpos)
        glCallList(part[radio_button_kaki_napak_variable.get()][i].gl_list) #set part i to the transformed position in opengl
        
#Inverse kinematic function
#Inverse kinematic for legs
def ik_tapakin(target_x, target_z, rotasi_tapak):
    print(target_x, target_z, rotasi_tapak)
    ''' 
    #brute force 2 (gagal, salah konsep)
    global page_step_rotasi
    global napak
    napak=True
    target_x=-50
    target_y=50
    target_z=120
    update_sudut_servo()
    f.transformasi(c.part)
    p=[]
    angle=[]
    for i in range(6):
        angle.append(0)
        p.append(0)
    p[0]=c.part[0][14].koordinat_sumbu_rotasi_servo_tertransformasi.elemen
    p[1]=c.part[0][18].koordinat_sumbu_rotasi_servo_tertransformasi.elemen
    p[2]=c.part[0][16].koordinat_sumbu_rotasi_servo_tertransformasi.elemen
    p[3]=c.part[0][20].koordinat_sumbu_rotasi_servo_tertransformasi.elemen
    p[4]=c.part[0][22].koordinat_sumbu_rotasi_servo_tertransformasi.elemen
    p[5]=c.part[0][24].koordinat_sumbu_rotasi_servo_tertransformasi.elemen
    d=[]
    r=[]
    r.append(14)
    r.append(18)
    r.append(16)
    r.append(20)
    r.append(22)
    r.append(24)
    for i in range(5):
        d.append(pow(pow(p[i+1][0][0]-p[i][0][0], 2)+pow(p[i+1][1][0]-p[i][1][0], 2)+pow(p[i+1][2][0]-p[i][2][0], 2), 1/2))
    t=[target_x, target_y, target_z]
    for i in range(5):
        b=0
        for j in range(37):
            j=(j-18)*10
            page_step_rotasi[int(entry_page.get())][int(entry_step.get())][r[i]]=j
            print(page_step_rotasi[int(entry_page.get())][int(entry_step.get())][r[i]])
            angle[i]=j
            update_sudut_servo()
            f.transformasi(c.part)
            for k in range(6):
                p[k]=c.part[0][r[k]].koordinat_sumbu_rotasi_servo_tertransformasi.elemen
                #print(p[k])
            dist=pow(pow(p[i+1][0][0]-t[0], 2)+pow(p[i+1][1][0]-t[1], 2)+pow(p[i+1][2][0]-t[2], 2), 1/2)
            d_total=0
            for k in range(i,5):
                d_total=d_total+d[k]
            print(dist, d_total)
            if(dist<d_total and b==0):
                a=1
                b=1
            elif(dist>d_total and b==0):
                a=0
                b=1
            #print("a", a, dist, d_total)
            if(a==1 and dist>d_total):
                #print(a, b, dist, d_total)
                break
            elif(a==0 and dist<d_total):
                print(a, b, dist, d_total)
                break
        
        b=0
        for j in range(angle[i]-10, angle[i]):
            #print("j=", j)
            page_step_rotasi[int(entry_page.get())][int(entry_step.get())][r[i]]=j
            update_sudut_servo()
            f.transformasi(c.part)
            for k in range(6):
                p[k]=c.part[0][r[k]].koordinat_sumbu_rotasi_servo_tertransformasi.elemen
            dist=pow(pow(p[i+1][0][0]-t[0], 2)+pow(p[i+1][1][0]-t[1], 2)+pow(p[i+1][2][0]-t[2], 2), 1/2)
            d_total=0
            for k in range(i,5):
                d_total=d_total+d[k]
            if(dist<d_total and b==0):
                a=1
                b=1
            elif(dist>d_total and b==0):
                a=0
                b=1
            if(a==1 and dist>d_total):
                page_step_rotasi[int(entry_page.get())][int(entry_step.get())][r[i]]=j-1
                update_sudut_servo()
                f.transformasi(c.part)
                break
            elif(a==0 and dist<d_total):
                
                break
        print(r[i], page_step_rotasi[int(entry_page.get())][int(entry_step.get())][r[i]])
    draw()
    '''
    '''
    #tinyik library (ga ada angle limit, terlalu simple)
    global napak
    napak=True
    update_sudut_servo()
    f.transformasi(c.part)
    p=[]
    angle=[]
    for i in range(6):
        angle.append(0)
        p.append(0)
    p[0]=c.part[0][14].koordinat_sumbu_rotasi_servo_tertransformasi.elemen
    p[1]=c.part[0][18].koordinat_sumbu_rotasi_servo_tertransformasi.elemen
    p[2]=c.part[0][16].koordinat_sumbu_rotasi_servo_tertransformasi.elemen
    p[3]=c.part[0][20].koordinat_sumbu_rotasi_servo_tertransformasi.elemen
    p[4]=c.part[0][22].koordinat_sumbu_rotasi_servo_tertransformasi.elemen
    p[5]=c.part[0][24].koordinat_sumbu_rotasi_servo_tertransformasi.elemen
    
    leg=tinyik.Actuator(['y', [p[0][0][0], p[0][1][0], p[0][2][0]], 'z', [p[1][0][0], p[1][1][0], p[1][2][0]], 'x', [p[2][0][0], p[2][1][0], p[2][2][0]], 'x', [p[3][0][0], p[3][1][0], p[3][2][0]], 'x', [p[4][0][0], p[4][1][0], p[4][2][0]], 'z', [p[5][0][0], p[5][1][0], p[5][2][0]]])
    leg.ee=[150,80,50]
    for i in range(6):
        angle[i]=numpy.rad2deg(leg.angles[i])
    page_step_rotasi[int(entry_page.get())][int(entry_step.get())][14]=angle[0]
    page_step_rotasi[int(entry_page.get())][int(entry_step.get())][18]=angle[1]
    page_step_rotasi[int(entry_page.get())][int(entry_step.get())][16]=angle[2]
    page_step_rotasi[int(entry_page.get())][int(entry_step.get())][20]=angle[3]
    page_step_rotasi[int(entry_page.get())][int(entry_step.get())][22]=angle[4]
    page_step_rotasi[int(entry_page.get())][int(entry_step.get())][24]=angle[5]
    
    draw()
    '''
    
    '''
    #fabrik method (orientation dan angle constraint belum)
    global napak
    
    napak=True
    update_sudut_servo()
    f.transformasi(c.part)
    n=6
    
    p=[]
    for i in range(n):
        p.append(0)
    p[0]=c.part[0][14].koordinat_sumbu_rotasi_servo_tertransformasi.elemen
    p[1]=c.part[0][18].koordinat_sumbu_rotasi_servo_tertransformasi.elemen
    p[2]=c.part[0][16].koordinat_sumbu_rotasi_servo_tertransformasi.elemen
    p[3]=c.part[0][20].koordinat_sumbu_rotasi_servo_tertransformasi.elemen
    p[4]=c.part[0][22].koordinat_sumbu_rotasi_servo_tertransformasi.elemen
    p[5]=c.part[0][24].koordinat_sumbu_rotasi_servo_tertransformasi.elemen
    
    d=[]
    for i in range(n-1):
        d.append(pow(pow(p[i+1][0][0]-p[i][0][0], 2)+pow(p[i+1][1][0]-p[i][1][0], 2)+pow(p[i+1][2][0]-p[i][2][0], 2), 1/2))
    
    d_total=0
    for i in range(n-1):
        d_total=d_total+d[i]
    
    t=[target_x, target_y, target_z]

    dist=pow(pow(p[0][0][0]-t[0], 2)+pow(p[0][1][0]-t[1], 2)+pow(p[0][2][0]-t[2], 2), 1/2)
    if dist>d_total:
        #target unreachable
        r=[]
        LAMBDA=[]
        for i in range(n-1):
            r.append(pow(pow(p[i][0][0]-t[0], 2)+pow(p[i][1][0]-t[1], 2)+pow(p[i][2][0]-t[2], 2), 1/2))
            LAMBDA.append(d[i]/r[i])
        for i in range(n-1):
            for j in range(3):
                p[i+1][j][0]=(1-LAMBDA[i])*p[i][j][0]+LAMBDA[i]*t[j]
                
    else:
        #target reachable
        b=[]
        for i in range(3):
            b.append(p[0][i][0])
        dif=(pow(pow(p[n-1][0][0]-t[0], 2)+pow(p[n-1][1][0]-t[1], 2)+pow(p[n-1][2][0]-t[2], 2), 1/2))
        tol=0.005
        m=0
        while dif>tol:
            print(m,dif)
            #forward reaching
            for i in range(3):
                p[n-1][i][0]=t[i]
            r=[]
            LAMBDA=[]
            for i in range(n-1):
                r.append(0)
                LAMBDA.append(0)
            for i in range(n-1):
                a=(n-1)-i-1
                r[a]=pow(pow(p[a+1][0][0]-p[a][0][0], 2)+pow(p[a+1][1][0]-p[a][1][0], 2)+pow(p[a+1][2][0]-p[a][2][0], 2), 1/2)
                LAMBDA[a]=d[a]/r[a]
                for j in range(3):
                    p[a][j][0]=(1-LAMBDA[a])*p[a+1][j][0]+LAMBDA[a]*p[a][j][0]
            #backward reaching
            for i in range(3):
                p[0][i][0]=b[i]
            for i in range(n-1):
                r[i]=pow(pow(p[i+1][0][0]-p[i][0][0], 2)+pow(p[i+1][1][0]-p[i][1][0], 2)+pow(p[i+1][2][0]-p[i][2][0], 2), 1/2)
                LAMBDA[i]=d[i]/r[i]
                for j in range(3):
                    p[i+1][j][0]=(1-LAMBDA[i])*p[i][j][0]+LAMBDA[i]*p[i+1][j][0]
                #angle limit
            dif=pow(pow(p[n-1][0][0]-t[0],2)+pow(p[n-1][1][0]-t[1],2)+pow(p[n-1][2][0]-t[2],2), 1/2)
            m=m+1
            time.sleep(1)
    #finding angle of each servo
    length_side=[0,0,0]
    angle=[]
    for i in range(n-2):
        angle.append(0)
    for i in range(n-2):
        length_side[0]=pow(pow(p[i+1][0][0]-p[i][0][0], 2)+pow(p[i+1][1][0]-p[i][1][0], 2)+pow(p[i+1][2][0]-p[i][2][0], 2), 1/2)
        length_side[1]=pow(pow(p[i+2][0][0]-p[i+1][0][0], 2)+pow(p[i+2][1][0]-p[i+1][1][0], 2)+pow(p[i+2][2][0]-p[i+1][2][0], 2), 1/2)
        length_side[2]=pow(pow(p[i][0][0]-p[i+2][0][0], 2)+pow(p[i][1][0]-p[i+2][1][0], 2)+pow(p[i][2][0]-p[i+2][2][0], 2), 1/2)
        d=(pow(length_side[0], 2)+pow(length_side[1], 2)-pow(length_side[2], 2))/(2*length_side[0]*length_side[1])
        if d<-1:
            d=d+0.00001
        elif d>1:
            d=d-0.00001
        angle.append(math.acos(d))
    page_step_rotasi[int(entry_page.get())][int(entry_step.get())][18]=angle[0]*57.2958-180
    page_step_rotasi[int(entry_page.get())][int(entry_step.get())][16]=angle[1]*57.2958-180
    page_step_rotasi[int(entry_page.get())][int(entry_step.get())][20]=angle[2]*57.2958-180
    page_step_rotasi[int(entry_page.get())][int(entry_step.get())][22]=angle[3]*57.2958-180
        
                    
    napak=True
    draw()
    '''
    '''
    #brute force try all combination (super very high computational cost)
    global napak
    alpha=0
    beta=-70
    gamma=-90
    pertambahan=10
    toleransi=20
    while(napak==False and alpha<=90):
        beta=-70
        while(napak==False and beta<=30):
            gamma=-90
            while(napak==False and gamma<=90):
                rotasi_servo[20]=alpha
                rotasi_servo[22]=beta
                rotasi_servo[24]=gamma
                update_sudut_servo()
                f.transformasi(c.part)
                print(alpha, beta, gamma)
                if(c.part[0][28].koordinat_titik_berat_tertransformasi.elemen[1][0]>=-toleransi and c.part[0][28].koordinat_titik_berat_tertransformasi.elemen[1][0]<=toleransi and c.part[0][29].koordinat_titik_berat_tertransformasi.elemen[1][0]>=-toleransi and c.part[0][29].koordinat_titik_berat_tertransformasi.elemen[1][0]<=toleransi and c.part[0][30].koordinat_titik_berat_tertransformasi.elemen[1][0]>=-toleransi and c.part[0][30].koordinat_titik_berat_tertransformasi.elemen[1][0]<=toleransi):
                    napak=True
                gamma=gamma+pertambahan
            beta=beta+pertambahan
        alpha=alpha+pertambahan'''
    
#draw to pygame opengl and tkinter canvas
def draw():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    canvas.delete("all")
    update_sudut_servo()
    f.transformasi(c.part)
    transformation()
    # render object to pygame opengl
    pygame.display.flip()
    #draw to tkinter canvas
    scale=3/4
    pos_x=200
    pos_z=75
    rad=15
    if(radio_button_kaki_napak_variable.get()==0):
        rect_L=canvas.create_rectangle(0*scale+pos_x,0*scale+pos_z,-100*scale+pos_x,150*scale+pos_z)
        line_L=canvas.create_line(c.part[0][28].koordinat_titik_berat_tertransformasi.elemen[0][0]*scale+pos_x, c.part[0][28].koordinat_titik_berat_tertransformasi.elemen[2][0]*scale+pos_z, c.part[0][29].koordinat_titik_berat_tertransformasi.elemen[0][0]*scale+pos_x, c.part[0][29].koordinat_titik_berat_tertransformasi.elemen[2][0]*scale+pos_z, c.part[0][30].koordinat_titik_berat_tertransformasi.elemen[0][0]*scale+pos_x, c.part[0][30].koordinat_titik_berat_tertransformasi.elemen[2][0]*scale+pos_z, c.part[0][31].koordinat_titik_berat_tertransformasi.elemen[0][0]*scale+pos_x, c.part[0][31].koordinat_titik_berat_tertransformasi.elemen[2][0]*scale+pos_z, c.part[0][28].koordinat_titik_berat_tertransformasi.elemen[0][0]*scale+pos_x, c.part[0][28].koordinat_titik_berat_tertransformasi.elemen[2][0]*scale+pos_z)
        circle_L=canvas.create_oval(f.titik_berat_x_L(c.part)*scale+pos_x-rad, f.titik_berat_z_L(c.part)*scale+pos_z-rad, f.titik_berat_x_L(c.part)*scale+pos_x+rad, f.titik_berat_z_L(c.part)*scale+pos_z+rad, fill=f._from_rgb((255,255,255)))
    else:
        rect_L=canvas.create_rectangle(0*scale+pos_x,0*scale+pos_z,-100*scale+pos_x,150*scale+pos_z)
        line_L=canvas.create_line(c.part[1][28].koordinat_titik_berat_tertransformasi.elemen[0][0]*scale+pos_x, c.part[1][28].koordinat_titik_berat_tertransformasi.elemen[2][0]*scale+pos_z, c.part[1][29].koordinat_titik_berat_tertransformasi.elemen[0][0]*scale+pos_x, c.part[1][29].koordinat_titik_berat_tertransformasi.elemen[2][0]*scale+pos_z, c.part[1][30].koordinat_titik_berat_tertransformasi.elemen[0][0]*scale+pos_x, c.part[1][30].koordinat_titik_berat_tertransformasi.elemen[2][0]*scale+pos_z, c.part[1][31].koordinat_titik_berat_tertransformasi.elemen[0][0]*scale+pos_x, c.part[1][31].koordinat_titik_berat_tertransformasi.elemen[2][0]*scale+pos_z, c.part[1][28].koordinat_titik_berat_tertransformasi.elemen[0][0]*scale+pos_x, c.part[1][28].koordinat_titik_berat_tertransformasi.elemen[2][0]*scale+pos_z)
        circle_L=canvas.create_oval(f.titik_berat_x_R(c.part)*scale+pos_x-rad, f.titik_berat_z_R(c.part)*scale+pos_z-rad, f.titik_berat_x_R(c.part)*scale+pos_x+rad, f.titik_berat_z_R(c.part)*scale+pos_z+rad, fill=f._from_rgb((255,255,255)))
    #for i in range(28):
    #    circle=canvas.create_oval(300/3+c.part[0][i].koordinat_titik_berat_tertransformasi.elemen[0][0]*3/5,11*300/12-c.part[0][i].koordinat_titik_berat_tertransformasi.elemen[1][0]*3/5,300/3+c.part[0][i].koordinat_titik_berat_tertransformasi.elemen[0][0]*3/5+(c.part[0][i].koordinat_titik_berat_tertransformasi.elemen[2][0]+300)/60,11*300/12-c.part[0][i].koordinat_titik_berat_tertransformasi.elemen[1][0]*3/5+(c.part[0][i].koordinat_titik_berat_tertransformasi.elemen[2][0]+300)/60, fill=f._from_rgb((255,255,255)))

#add gui to tkinter
root=Tk()
root.title("Simulator")
root.geometry("350x650")

frame_controller=Frame(root, width=300, height=450)
frame_controller.grid(row=0, column=0)

label_space=Label(frame_controller, text=" ")
label_space.grid(row=0,column=0)

radio_button_kaki_napak_variable=IntVar()
radio_button_kaki_napak_variable.set(0)
radio_button_kaki_kiri_napak=Radiobutton(frame_controller, text="kaki kiri napak", variable=radio_button_kaki_napak_variable ,value=0, command=lambda:draw())
radio_button_kaki_kiri_napak.grid(row=1, column=0)
radio_button_kaki_kanan_napak=Radiobutton(frame_controller, text="kaki kanan napak", variable=radio_button_kaki_napak_variable ,value=1, command=lambda:draw())
radio_button_kaki_kanan_napak.grid(row=1, column=1)

label_no_servo=Label(frame_controller, text="no servo:")
label_no_servo.grid(row=2,column=0)

no_servo_variable = StringVar()
entry_no_servo=Entry(frame_controller, textvariable=no_servo_variable)
entry_no_servo.grid(row=2, column=1)
no_servo_variable.set("26")

#rotasi_servo_variable=StringVar()
label_rotasi_servo=Label(frame_controller)
label_rotasi_servo.grid(row=3, column=0)

slider_rotasi_servo=Scale(frame_controller, orient=HORIZONTAL, command=slide_servo, length=200, from_=-180, to=180, showvalue=0)
slider_rotasi_servo.grid(row=3,column=1)

label_tx=Label(frame_controller, text="x:")
label_tx.grid(row=4, column=0)

slider_tx=Scale(frame_controller, orient=HORIZONTAL, command=slide_tx, length=200, from_=-3000, to=7000, showvalue=0)
slider_tx.grid(row=4, column=1)
slider_tx.set(2000)

label_tx=Label(frame_controller, text="y:")
label_tx.grid(row=5, column=0)

slider_ty=Scale(frame_controller, orient=HORIZONTAL, command=slide_ty, length=200, from_=-10000, to=0, showvalue=0)
slider_ty.grid(row=5, column=1)
slider_ty.set(-5000)

label_scale=Label(frame_controller, text="scale:")
label_scale.grid(row=6, column=0)

slider_scale=Scale(frame_controller, orient=HORIZONTAL, command=slide_scale, length=200, from_=100, to=500, showvalue=0)
slider_scale.grid(row=6, column=1)
slider_scale.set(500)

label_page=Label(frame_controller, text="page:")
label_page.grid(row=7, column=0)

entry_page_variable=IntVar()
entry_page=Entry(frame_controller, textvariable=entry_page_variable)
entry_page.grid(row=7, column=1)
entry_page_variable.set("1")

label_step=Label(frame_controller, text="step:")
label_step.grid(row=8, column=0)

entry_step_variable=IntVar()
entry_step=Entry(frame_controller, textvariable=entry_step_variable)
entry_step.grid(row=8, column=1)
entry_step_variable.set("1")
'''
button_save_temp_page_and_step=Button(frame_controller, text="save temp page & step", command=lambda:save_temp_page_and_step())
button_save_page_and_step.grid(row=9, column=0)

button_load_page_and_step=Button(frame_controller, text="load page & step", command=lambda:load_page_and_step)
button_load_page_and_step.grid(row=9, column=1)'''

label_step_time=Label(frame_controller, text="step time")
label_step_time.grid(row=9, column=0)
'''
entry_step_time_variable=IntVar()
entry_step_time=Entry(frame_controller, textvariable=entry_step_time_variable)
entry_step_time.grid(row=9, column=1)
entry_step_time_variable.set("25")
'''
slider_step_time=Scale(frame_controller, orient=HORIZONTAL, command=slide_step_time, length=200, from_=25, to=1000, resolution=5)
slider_step_time.grid(row=9, column=1)

label_posisi_tapak_x=Label(frame_controller, text="ik napak:")
label_posisi_tapak_x.grid(row=10, column=0)

label_posisi_tapak_x=Label(frame_controller, text="posisi tapak x:")
label_posisi_tapak_x.grid(row=11, column=0)

entry_posisi_tapak_x_variable=IntVar()
entry_posisi_tapak_x=Entry(frame_controller, textvariable=entry_posisi_tapak_x_variable)
entry_posisi_tapak_x.grid(row=11, column=1)
entry_posisi_tapak_x_variable.set("110")

label_posisi_tapak_z=Label(frame_controller, text="posisi tapak z:")
label_posisi_tapak_z.grid(row=12, column=0)

entry_posisi_tapak_z_variable=IntVar()
entry_posisi_tapak_z=Entry(frame_controller, textvariable=entry_posisi_tapak_z_variable)
entry_posisi_tapak_z.grid(row=12, column=1)
entry_posisi_tapak_z_variable.set("0")

label_rotasi_tapak=Label(frame_controller, text="rotasi tapak:")
label_rotasi_tapak.grid(row=13, column=0)

entry_rotasi_tapak_variable=IntVar()
entry_rotasi_tapak=Entry(frame_controller, textvariable=entry_rotasi_tapak_variable)
entry_rotasi_tapak.grid(row=13, column=1)
entry_rotasi_tapak_variable.set("0")

button_save_current_page=Button(frame_controller, text="tapakin", command=lambda:ik_tapakin(int(entry_posisi_tapak_x.get()), int(entry_posisi_tapak_z.get()), int(entry_rotasi_tapak.get())))
button_save_current_page.grid(row=14, column=1)

button_save_current_page=Button(frame_controller, text="save(belum)", command=lambda:save_all())
button_save_current_page.grid(row=15, column=0)

label_titik_berat=Label(frame_controller, text="ZMP(masih COG):")
label_titik_berat.grid(row=16, column=0)

frame_canvas=Frame(root, width=350, height=250)
frame_canvas.grid(row=1, column=0)

canvas=Canvas(frame_canvas, width=350, height=250, bg=f._from_rgb((75,120,75)))
canvas.grid(row=0, column=0)

draw() #draw to pygame opengl and tkinter canvas for the first time

#looping pygame with pygame clock
while 1:
    clock.tick(30)
    try: #handle error input
        update_sudut_servo()
        if(int(entry_no_servo.get())<=12):
            label_rotasi_servo.config(text=str(round(page_step_rotasi[int(entry_page.get())][int(entry_step.get())][int(entry_no_servo.get())]*512/180 +512)))
        else:
            label_rotasi_servo.config(text=str(round(page_step_rotasi[int(entry_page.get())][int(entry_step.get())][int(entry_no_servo.get())]*2048/180 +2048)))
        slider_rotasi_servo.set(rotasi_servo[int(entry_no_servo.get())])
        
        update_step_time()
        slider_step_time.set(step_time)
        
        '''
        update_step_time()
        entry_step_time_variable.set(step_time[int(entry_page.get())][int(entry_step.get())])
        '''
        draw()
    except:
        print("input page/step/no servo salah")
        
    root.update() #update tkinter inside pygame loop
    
    