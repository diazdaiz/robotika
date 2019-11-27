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
import time

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

move=False
page_step_rotasi=[]
rotasi_servo=[]
for i in range(27):
    rotasi_servo.append(0)
    
for i in range(151):
    mtemp_2=[]
    for j in range(20):
        mtemp_1=[]
        for k in range(27):
            mtemp_1.append(0)
        mtemp_1.append(0) #step pause
        mtemp_1.append(40) #step time
        mtemp_1.append("null") #step name
        mtemp_1.append(0) #step repeat
        mtemp_1.append(20) #played step
        mtemp_1.append(0) #page next
        for k in range(27):
            mtemp_1.append(0) #step frame
        for k in range(27):
            mtemp_1.append(0) #frame transition
        mtemp_2.append(mtemp_1)
    page_step_rotasi.append(mtemp_2)

#load page_data
def load_page():
    for i in range(1, 151):
        file=open("page_data\\"+str(i), "r")
        k=0
        for line in file:
            token=line.split("\n")
            token=token[0].split(",")
            #print(len(token))
            #print(k)
            for j in range(20):
                if(k<=12):
                    page_step_rotasi[i][j][k]=int((int(token[j])-512)*180/512)
                elif(k<=26):
                    page_step_rotasi[i][j][k]=int((int(token[j])-2048)*180/2048)
                elif(k==29):
                    page_step_rotasi[i][j][k]=token[j]
                else:
                    page_step_rotasi[i][j][k]=int(token[j])
            k=k+1
        '''for line in file:
            token=line.split(",")
            print(token)'''
        
        file.close()
    
load_page()

#tkinter widget function
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
    rotasi_servo[int(entry_no_servo.get())]=int(val)
    page_step_rotasi[int(entry_page.get())][int(entry_step.get())][int(entry_no_servo.get())]=rotasi_servo[int(entry_no_servo.get())]
    
def set_name(name):
    for i in range(20):    
        page_step_rotasi[int(entry_page.get())][i][29]=name
    
def set_played_step(played_step):
    for i in range(20): 
        page_step_rotasi[int(entry_page.get())][i][31]=int(played_step)
    
def set_repeat(page_repeat):
    for i in range(20): 
        page_step_rotasi[int(entry_page.get())][i][30]=int(page_repeat)

def set_next_page(next_page):
    for i in range(20): 
        page_step_rotasi[int(entry_page.get())][i][32]=int(next_page)
        
def slide_step_frame(val):
    page_step_rotasi[int(entry_page.get())][int(entry_step.get())][int(entry_no_servo.get())+33]=int(val)
    
def menu_button_frame_transition_command_0():
    page_step_rotasi[int(entry_page.get())][int(entry_step.get())][int(entry_no_servo.get())+60]=0
    
def menu_button_frame_transition_command_1():
    page_step_rotasi[int(entry_page.get())][int(entry_step.get())][int(entry_no_servo.get())+60]=1
    
def menu_button_frame_transition_command_2():
    page_step_rotasi[int(entry_page.get())][int(entry_step.get())][int(entry_no_servo.get())+60]=2
    
def menu_button_frame_transition_command_3():
    page_step_rotasi[int(entry_page.get())][int(entry_step.get())][int(entry_no_servo.get())+60]=3
    
def set_time(step_time):
    page_step_rotasi[int(entry_page.get())][int(entry_step.get())][28]=int(step_time)
    
def set_pause(step_pause):
    page_step_rotasi[int(entry_page.get())][int(entry_step.get())][27]=int(step_pause)

def save_all():
    for i in range(1, 151):
        file=open("page_data\\"+str(i), "w")
        for j in range(33):
            for k in range(20):
                if(k<=18):
                    if(j<=12):
                        file.write(str(int(page_step_rotasi[i][k][j]*512/180+512))+",")
                    elif(j<=26):
                        file.write(str(int(page_step_rotasi[i][k][j]*2048/180+2048))+",")
                    else:
                        file.write(str(page_step_rotasi[i][k][j])+",")
                elif(k==19):
                    if(j<=12):
                        file.write(str(int(page_step_rotasi[i][k][j]*512/180+512))+"\n")
                    elif(j<=26):
                        file.write(str(int(page_step_rotasi[i][k][j]*2048/180+2048))+"\n")
                    else:
                        file.write(str(page_step_rotasi[i][k][j])+"\n")
        file.close()
        
def play():
    global move
    move=True
    page=int(entry_page.get())
    step=int(entry_step.get())
    while move==True and page!=0:
        i=0
        while i<page_step_rotasi[page][step][30]+1:
            print(i)
            entry_page_variable.set(page)
            entry_step_variable.set(step)
            draw()
            time.sleep(page_step_rotasi[page][step][28]/1000)
            time.sleep(page_step_rotasi[page][step][27]/1000)
            if(step+1<page_step_rotasi[page][step][31]):
                step=step+1
            else:
                i=i+1
                step=0
                if(i==page_step_rotasi[page][step][30]+1):
                    page=page_step_rotasi[page][step][32]
        
def stop():
    global move
    move=False
    
#translate frame function
def translate_frame():
    cek_page=[]
    for i in range(151):
        cek_page.append(False)
    chain=[]
    for j in range(27):
        for i in range(1, 151):
            page=i
            chain_temp_0=[]
            for k in range(20):
                if(cek_page[i]==False and page_step_rotasi[i][k][33+j]==True):
                    while(page!=0):
                        cek_page[page]=True
                        chain_temp_1=[]
                        chain_temp_1.append(j)
                        chain_temp_1.append(page)
                        chain_temp_1.append(k)
                        chain_temp_1.append(page_step_rotasi[page][k][33+j])
                        chain_temp_0.append(chain_temp_1)
                        if(k==(page_step_rotasi[page][0][31]-1)):
                            k=-1
                            page=page_step_rotasi[page][0][32]
                        k=k+1
                    chain.append(chain_temp_0)
        for i in range(1, 151):
            cek_page[i]=False
    print(chain)
    print(chain[0])
    print(chain[0][0])
    print(len(chain))
    frame_in_chain=[]
    for i in range(len(chain)):
        temp_0=[]
        temp_1=0
        temp_2=0
        begin_chain=True
        for j in range(len(chain[i])):
            print(i, j, chain[i][j][3])
            if(chain[i][j][3]==1):
                temp_1=temp_1+1
                if(begin_chain==False):
                    temp_0.append(temp_2)
                    temp_2=0
                begin_chain=False
            if(chain[i][j][3]==0):
                temp_2=temp_2+1
        temp_0.append(temp_1)
        frame_in_chain.append(temp_0)
    print(frame_in_chain)
    for i in range(len(frame_in_chain)):
        for j in range(frame_in_chain[i][len(frame_in_chain[i])-1]-1):
            for k in range(frame_in_chain[i][j]):
                sequence=1
                for l in range(j):
                    sequence=sequence+frame_in_chain[i][j-1]+1
                print(i, j, sequence, frame_in_chain[i][j])
                print(chain[i][sequence+frame_in_chain[i][j]][1])
                print(chain[i][sequence+frame_in_chain[i][j]][2])
                print(chain[i][sequence+frame_in_chain[i][j]][0])
                print(chain[i][sequence-1][1])
                print(chain[i][sequence-1][2])
                print(chain[i][sequence-1][0])
                print(page_step_rotasi[chain[i][sequence-1][1]][chain[i][sequence-1][2]][chain[i][sequence-1][0]], "+", ((k+1)/(frame_in_chain[i][j]+1))*(page_step_rotasi[chain[i][sequence+frame_in_chain[i][j]][1]][chain[i][sequence+frame_in_chain[i][j]][2]][chain[i][sequence+frame_in_chain[i][j]][0]]-page_step_rotasi[chain[i][sequence-1][1]][chain[i][sequence-1][2]][chain[i][sequence-1][0]]))
                print(((k+1)/(frame_in_chain[i][j]+1)),"*(",page_step_rotasi[chain[i][sequence+frame_in_chain[i][j]][1]][chain[i][sequence+frame_in_chain[i][j]][2]][chain[i][sequence+frame_in_chain[i][j]][0]], "-", page_step_rotasi[chain[i][sequence-1][1]][chain[i][sequence-1][2]][chain[i][sequence-1][0]],")")
                page_step_rotasi[chain[i][sequence+k][1]][chain[i][sequence+k][2]][chain[i][sequence+k][0]]=page_step_rotasi[chain[i][sequence-1][1]][chain[i][sequence-1][2]][chain[i][sequence-1][0]]+((k+1)/(frame_in_chain[i][j]+1))*(page_step_rotasi[chain[i][sequence+frame_in_chain[i][j]][1]][chain[i][sequence+frame_in_chain[i][j]][2]][chain[i][sequence+frame_in_chain[i][j]][0]]-page_step_rotasi[chain[i][sequence-1][1]][chain[i][sequence-1][2]][chain[i][sequence-1][0]])
    

#transformation function
def transformation_0(kaki, pe, di, ur): #pentransformasi, ditrasformasi, urutan
    glTranslate(c.part[kaki][pe].koordinat_sumbu_rotasi_servo.elemen[0][0]+tx/20, c.part[kaki][pe].koordinat_sumbu_rotasi_servo.elemen[1][0]+ty/20, c.part[kaki][pe].koordinat_sumbu_rotasi_servo.elemen[2][0]-zpos)
    if(pe==0 or pe==3 or pe==4 or pe==7 or pe==8 or pe==16 or pe==17 or pe==20 or pe==21 or pe==22 or pe==23):
        if(kaki==0 and (pe==0 or pe==16 or pe==17 or pe==20 or pe==21 or pe==22 or pe==23)):
            glRotatef(rotasi_servo[pe],1,0,0)
        elif(kaki==0 and(pe==3 or pe==4)):
            glRotatef(rotasi_servo[pe]-90,1,0,0)
        elif(kaki==0 and (pe==7 or pe==8)):
            glRotatef(rotasi_servo[pe]+90,1,0,0)
        elif(kaki==0):
            glRotatef(-rotasi_servo[pe],1,0,0)
        elif(kaki==1 and (pe==0 or pe==3 or pe==4 or pe==7 or pe==8)):
            glRotatef(rotasi_servo[pe],1,0,0)
        elif(kaki==1 and(pe==3 or pe==4)):
            glRotatef(rotasi_servo[pe]-90,1,0,0)
        elif(kaki==1 and (pe==7 or pe==8)):
            glRotatef(rotasi_servo[pe]+90,1,0,0)
        elif(kaki==1 and (pe==16 or pe==17 or pe==20 or pe==21 or pe==22 or pe==23)):
            glRotatef(-rotasi_servo[pe],1,0,0)
    elif(pe==2 or pe==9 or pe==10 or pe==11 or pe==12 or pe==13 or pe==14 or pe==15):
        if(kaki==0 and (pe==2 or pe==9 or pe==10 or pe==11 or pe==12 or pe==13 or pe==14 or pe==15)):
            glRotatef(rotasi_servo[pe],0,1,0)
        elif(kaki==0):
            glRotatef(-rotasi_servo[pe],0,1,0)
        elif(kaki==1 and (pe==2 or pe==9 or pe==10 or pe==11 or pe==12 or pe==13)):
            glRotatef(rotasi_servo[pe],0,1,0)
        elif(kaki==1 and (pe==14 or pe==15)):
            glRotatef(-rotasi_servo[pe],0,1,0)
    elif(pe==1 or pe==5 or pe==6 or pe==18 or pe==19 or pe==24 or pe==25 or pe==26):
        if(kaki==0 and (pe==1 or pe==5 or pe==6 or pe==18 or pe==19 or pe==24 or pe==25 or pe==26)):
            glRotatef(rotasi_servo[pe],0,0,1)
        elif(kaki==0):
            glRotatef(-rotasi_servo[pe],0,0,1)
        elif(kaki==1 and (pe==1 or pe==5 or pe==6 or pe==26)):
            glRotatef(rotasi_servo[pe],0,0,1)
        elif(kaki==1 and (pe==18 or pe==19 or pe==24 or pe==25)):
            glRotatef(-rotasi_servo[pe],0,0,1)
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
    scale=2/5
    pos_x=200
    pos_z=35
    rad=10
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
root.geometry("400x700")

frame_controller=Frame(root, width=300, height=450)
frame_controller.grid(row=0, column=0)

label_info=Label(frame_controller, text=" ")
label_info.grid(row=0,column=0, columnspan=3)

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

label_rotasi_servo=Label(frame_controller)
label_rotasi_servo.grid(row=3, column=0)

slider_rotasi_servo=Scale(frame_controller, orient=HORIZONTAL, command=slide_servo, length=200, from_=-180, to=180, showvalue=0)
slider_rotasi_servo.grid(row=3, column=1, columnspan=2)

label_tx=Label(frame_controller, text="x:")
label_tx.grid(row=4, column=0)

slider_tx=Scale(frame_controller, orient=HORIZONTAL, command=slide_tx, length=200, from_=-3000, to=7000, showvalue=0)
slider_tx.grid(row=4, column=1, columnspan=2)
slider_tx.set(2000)

label_tx=Label(frame_controller, text="y:")
label_tx.grid(row=5, column=0)

slider_ty=Scale(frame_controller, orient=HORIZONTAL, command=slide_ty, length=200, from_=-10000, to=0, showvalue=0)
slider_ty.grid(row=5, column=1, columnspan=2)
slider_ty.set(-5000)

label_scale=Label(frame_controller, text="scale:")
label_scale.grid(row=6, column=0)

slider_scale=Scale(frame_controller, orient=HORIZONTAL, command=slide_scale, length=200, from_=100, to=500, showvalue=0)
slider_scale.grid(row=6, column=1, columnspan=2)
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
entry_step_variable.set("0")

label_page_name=Label(frame_controller, text="page name")
label_page_name.grid(row=9, column=0)

entry_page_name_variable=IntVar()
entry_page_name=Entry(frame_controller, textvariable=entry_page_name_variable)
entry_page_name.grid(row=9, column=1)
entry_page_name_variable.set("null")

button_page_name=Button(frame_controller, text="set name", command=lambda:set_name(entry_page_name.get()))
button_page_name.grid(row=9, column=2, sticky=W)

label_played_step=Label(frame_controller, text=" played step page")
label_played_step.grid(row=10, column=0)

entry_played_step_variable=IntVar()
entry_played_step=Entry(frame_controller, textvariable=entry_played_step_variable)
entry_played_step.grid(row=10, column=1)
entry_played_step_variable.set("20")

button_played_step=Button(frame_controller, text="set played step", command=lambda:set_played_step(entry_played_step.get()))
button_played_step.grid(row=10, column=2, sticky=W)

label_page_repeat=Label(frame_controller, text="page repeat")
label_page_repeat.grid(row=11, column=0)

entry_page_repeat_variable=IntVar()
entry_page_repeat=Entry(frame_controller, textvariable=entry_page_repeat_variable)
entry_page_repeat.grid(row=11, column=1)
entry_page_repeat_variable.set("0")

button_page_repeat=Button(frame_controller, text="set repeat", command=lambda:set_repeat(entry_page_repeat.get()))
button_page_repeat.grid(row=11, column=2, sticky=W)

label_next_page=Label(frame_controller, text="next page")
label_next_page.grid(row=12, column=0)

entry_next_page_variable=IntVar()
entry_next_page=Entry(frame_controller, textvariable=entry_next_page_variable)
entry_next_page.grid(row=12, column=1)
entry_next_page_variable.set("0")

button_next_page=Button(frame_controller, text="set next page", command=lambda:set_next_page(entry_next_page.get()))
button_next_page.grid(row=12, column=2, sticky=W)

label_step_frame=Label(frame_controller, text="step frame")
label_step_frame.grid(row=13, column=0)

slider_step_frame=Scale(frame_controller, orient=HORIZONTAL, command=slide_step_frame, length=60, from_=0, to=1, showvalue=0)
slider_step_frame.grid(row=13, column=1)

label_step_frame_value=Label(frame_controller, text="")
label_step_frame_value.grid(row=13, column=2)

label_frame_transition=Label(frame_controller, text="frame transition")
label_frame_transition.grid(row=14, column=0)

menu_button_frame_transition=Menubutton(frame_controller, text="select frame transition")
menu_button_frame_transition.menu=Menu(menu_button_frame_transition)
menu_button_frame_transition["menu"]=menu_button_frame_transition.menu
menu_button_frame_transition.menu.add_command(label="linear", command=lambda: menu_button_frame_transition_command_0())
menu_button_frame_transition.menu.add_command(label="ease in", command=lambda: menu_button_frame_transition_command_1())
menu_button_frame_transition.menu.add_command(label="ease out", command=lambda: menu_button_frame_transition_command_2())
menu_button_frame_transition.menu.add_command(label="ease in and out", command=lambda: menu_button_frame_transition_command_3())
menu_button_frame_transition.grid(row=14, column=1)

label_frame_transition_value=Label(frame_controller, text="")
label_frame_transition_value.grid(row=14, column=2)

label_step_time=Label(frame_controller, text="step time")
label_step_time.grid(row=15, column=0)

entry_step_time_variable=IntVar()
entry_step_time=Entry(frame_controller, textvariable=entry_step_time_variable)
entry_step_time.grid(row=15, column=1)
entry_step_time_variable.set("25")

button_step_time=Button(frame_controller, text="set time", command=lambda:set_time(entry_step_time.get()))
button_step_time.grid(row=15, column=2, sticky=W)

label_step_pause=Label(frame_controller, text="step pause")
label_step_pause.grid(row=16, column=0)

entry_step_pause_variable=IntVar()
entry_step_pause=Entry(frame_controller, textvariable=entry_step_pause_variable)
entry_step_pause.grid(row=16, column=1)
entry_step_pause_variable.set("0")

button_step_pause=Button(frame_controller, text="set pause", command=lambda:set_pause(entry_step_pause.get()))
button_step_pause.grid(row=16, column=2, sticky=W)

button_translate_frame=Button(frame_controller, text="translate frame", command=lambda:translate_frame())
button_translate_frame.grid(row=17, column=0)

button_play=Button(frame_controller, text="play", command=lambda:play())
button_play.grid(row=17, column=1)

button_stop=Button(frame_controller, text="stop", command=lambda:stop())
button_stop.grid(row=17, column=2, sticky=W)

label_posisi_tapak_x=Label(frame_controller, text="ik napak(belum):")
label_posisi_tapak_x.grid(row=18, column=0)

button_save_current_page=Button(frame_controller, text="tapakin", command=lambda:ik_tapakin(int(entry_posisi_tapak_x.get()), int(entry_posisi_tapak_z.get()), int(entry_rotasi_tapak.get())))
button_save_current_page.grid(row=18, column=1, sticky=W)

label_posisi_tapak_x=Label(frame_controller, text="posisi tapak x:")
label_posisi_tapak_x.grid(row=19, column=0)

entry_posisi_tapak_x_variable=IntVar()
entry_posisi_tapak_x=Entry(frame_controller, textvariable=entry_posisi_tapak_x_variable)
entry_posisi_tapak_x.grid(row=19, column=1)
entry_posisi_tapak_x_variable.set("110")

label_posisi_tapak_z=Label(frame_controller, text="posisi tapak z:")
label_posisi_tapak_z.grid(row=20, column=0)

entry_posisi_tapak_z_variable=IntVar()
entry_posisi_tapak_z=Entry(frame_controller, textvariable=entry_posisi_tapak_z_variable)
entry_posisi_tapak_z.grid(row=20, column=1)
entry_posisi_tapak_z_variable.set("0")

label_rotasi_tapak=Label(frame_controller, text="rotasi tapak:")
label_rotasi_tapak.grid(row=21, column=0)

entry_rotasi_tapak_variable=IntVar()
entry_rotasi_tapak=Entry(frame_controller, textvariable=entry_rotasi_tapak_variable)
entry_rotasi_tapak.grid(row=21, column=1)
entry_rotasi_tapak_variable.set("0")

button_save_current_page=Button(frame_controller, text="save", command=lambda:save_all())
button_save_current_page.grid(row=22, column=0)

label_titik_berat=Label(frame_controller, text="ZMP(masih COG):")
label_titik_berat.grid(row=23, column=0)

frame_canvas=Frame(root, width=350, height=250)
frame_canvas.grid(row=1, column=0)

canvas=Canvas(frame_canvas, width=400, height=200, bg=f._from_rgb((75,120,75)))
canvas.grid(row=0, column=0)

draw() #draw to pygame opengl and tkinter canvas for the first time

#looping pygame with pygame clock
while 1:
    clock.tick(30)
    try: #handle error input
        label_info.config(text=str(page_step_rotasi[int(entry_page.get())][int(entry_step.get())][29])+", played_step="+str(page_step_rotasi[int(entry_page.get())][int(entry_step.get())][31])+", repeat="+str(page_step_rotasi[int(entry_page.get())][int(entry_step.get())][30])+", next="+str(page_step_rotasi[int(entry_page.get())][int(entry_step.get())][32])+", time="+str(page_step_rotasi[int(entry_page.get())][int(entry_step.get())][28])+", pause="+str(page_step_rotasi[int(entry_page.get())][int(entry_step.get())][27]))
        update_sudut_servo()
        if(int(entry_no_servo.get())<=12):
            label_rotasi_servo.config(text=str(round(page_step_rotasi[int(entry_page.get())][int(entry_step.get())][int(entry_no_servo.get())]*512/180 +512)))
        else:
            label_rotasi_servo.config(text=str(round(page_step_rotasi[int(entry_page.get())][int(entry_step.get())][int(entry_no_servo.get())]*2048/180 +2048)))
        slider_rotasi_servo.set(rotasi_servo[int(entry_no_servo.get())])
        slider_step_frame.set(page_step_rotasi[int(entry_page.get())][int(entry_step.get())][int(entry_no_servo.get())+33])
        if(page_step_rotasi[int(entry_page.get())][int(entry_step.get())][int(entry_no_servo.get())+33]==0):
            label_step_frame_value.config(text="False")
        else:
            label_step_frame_value.config(text="True")
        draw()
        if(page_step_rotasi[int(entry_page.get())][int(entry_step.get())][int(entry_no_servo.get())+60]==0):
            label_frame_transition_value.config(text="linear")
        elif(page_step_rotasi[int(entry_page.get())][int(entry_step.get())][int(entry_no_servo.get())+60]==1):
            label_frame_transition_value.config(text="ease in")
        elif(page_step_rotasi[int(entry_page.get())][int(entry_step.get())][int(entry_no_servo.get())+60]==2):
            label_frame_transition_value.config(text="ease out")
        elif(page_step_rotasi[int(entry_page.get())][int(entry_step.get())][int(entry_no_servo.get())+60]==3):
            label_frame_transition_value.config(text="ease in and out")
    except:
        print("input page/step/no servo salah")
        
    root.update() #update tkinter inside pygame loop
    
    