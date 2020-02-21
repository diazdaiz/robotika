# Basic OBJ file viewer. needs objloader from:
#  http://www.pygame.org/wiki/OBJFileLoader
import sys, pygame
from pygame.locals import *
from pygame.constants import *
from OpenGL.GL import *
from OpenGL.GLU import *
import Fungsi as f
import Class as c
import pdb
import math
import numpy as np
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
#c.Part.load_data()  

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
for i in range(28):
    rotasi_servo.append(0)
    
for i in range(151):
    mtemp_2=[]
    for j in range(20):
        mtemp_1=[]
        for k in range(27):
            mtemp_1.append(0)
        mtemp_1.append(0) #step pause
        mtemp_1.append(5) #step time
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
    
step_rotation_copy=[]
for i in range(27):
    step_rotation_copy.append(0)

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
                    page_step_rotasi[i][j][k]=int((float(token[j])-512)*180/512)
                elif(k<=26):
                    page_step_rotasi[i][j][k]=int((float(token[j])-2048)*180/2048)
                #elif(k==28):
                    #page_step_rotasi[i][j][k]=5
                elif(k==29):
                    page_step_rotasi[i][j][k]=token[j]
                else:
                    page_step_rotasi[i][j][k]=int(token[j])
            k=k+1
        file.close()
        file=open("page_data\\frame_"+str(i), "r")
        k=0
        for line in file:
            token=line.split("\n")
            token=token[0].split(",")
            #print(len(token))
            #print(k)
            for j in range(20):
                page_step_rotasi[i][j][k+33]=int(token[j])
            k=k+1
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
        c.arana.part["kiri"][i].M_rotasi=f.matriks_rotasi(c.arana.part["kiri"][i].sumbu, rotasi_servo[i], c.arana.part["kiri"][i].arah_rotasi, c.arana.part["kiri"][i].sudut_awal_rotasi)
        c.arana.part["kanan"][i].M_rotasi=f.matriks_rotasi(c.arana.part["kanan"][i].sumbu, rotasi_servo[i], c.arana.part["kanan"][i].arah_rotasi, c.arana.part["kanan"][i].sudut_awal_rotasi)
    
    for i in range(27, 32):
        c.arana.part["kiri"][i].M_rotasi=f.matriks_identitas()
        c.arana.part["kanan"][i].M_rotasi=f.matriks_identitas()
    
def slide_servo(val):
    rotasi_servo[int(entry_no_servo.get())]=int(val)
    page_step_rotasi[int(entry_page.get())][int(entry_step.get())][int(entry_no_servo.get())]=rotasi_servo[int(entry_no_servo.get())]
    
def copy_step():
    for i in range(27):
        step_rotation_copy[i]=page_step_rotasi[int(entry_page.get())][int(entry_step.get())][i]
        
def paste_step():
    for i in range(27):
        page_step_rotasi[int(entry_page.get())][int(entry_step.get())][i]=step_rotation_copy[i]
    
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
    for i in range(1, 151):
        file=open("page_data\\frame_"+str(i), "w")
        for j in range(27):
            for k in range(20):
                if(k<=18):
                    file.write(str(page_step_rotasi[i][k][j+33])+",")
                elif(k==19):
                    file.write(str(page_step_rotasi[i][k][j+33])+"\n")
        for j in range(27):
            for k in range(20):
                if(k<=18):
                    file.write(str(page_step_rotasi[i][k][j+60])+",")
                elif(k==19):
                    file.write(str(page_step_rotasi[i][k][j+60])+"\n")
        file.close()
        
def play():
    global move
    move=True
    chain=[]
    page=int(entry_page.get())
    step=int(entry_step.get())
    page_temp=page
    step_temp=step
    t_0=time.process_time()
    while page!=0:
        i=0
        while i<page_step_rotasi[page][step][30]+1:
            chain_temp=[]
            chain_temp.append(page)
            chain_temp.append(step)
            chain_temp.append(page_step_rotasi[page][step][28])
            chain_temp.append(page_step_rotasi[page][step][27])
            if(step+1<page_step_rotasi[page][step][31]):
                step=step+1
                chain.append(chain_temp)
            else:
                chain.append(chain_temp)
                i=i+1
                step=0
                if(i==page_step_rotasi[page][step][30]+1):
                    page=page_step_rotasi[page][step][32]
    print(chain)
    time_total=0
    pembagi_waktu=125
    for i in range(len(chain)):
        time_total=time_total+chain[i][2]/pembagi_waktu+chain[i][3]/pembagi_waktu
    while time.process_time()-t_0<time_total and move==True:
        time_temp=0
        i=0
        while time_temp<(time.process_time()-t_0):
            try:
                time_temp=time_temp+chain[i][2]/pembagi_waktu+chain[i][3]/pembagi_waktu
                i=i+1
            except:
                break
        i=i-1
        time_temp=time_temp-chain[i][3]/pembagi_waktu
        for j in range(27):
            try:
                if(((time.process_time()-t_0-time_temp))/(chain[i][2]/pembagi_waktu)+2-((chain[i][2]+chain[i][3])/(chain[i][2]))>0):
                    page_step_rotasi[0][0][j]=page_step_rotasi[chain[i][0]][chain[i][1]][j]+((time.process_time()-t_0-time_temp)/(chain[i][2]/pembagi_waktu)+2-((chain[i][2]+chain[i][3])/(chain[i][2])))*(page_step_rotasi[chain[i+1][0]][chain[i+1][1]][j]-page_step_rotasi[chain[i][0]][chain[i][1]][j])
            except:
                pass
        entry_page_variable.set(0)
        entry_step_variable.set(0)
        draw()
        '''
        time_temp=0
        i=0
        while time_temp<(time.process_time()-t_0):
            try:
                time_temp=time_temp+chain[i][2]/pembagi_waktu+chain[i][3]/pembagi_waktu
                i=i+1
            except:
                break               
        i=i-1
        
        entry_page_variable.set(0)
        entry_step_variable.set(0)
        draw()
        '''
        #print(time.process_time()-t_0)
        print("i=", i,", page: ", chain[i][0], ", step: ", chain[i][1])
        print(((time.process_time()-t_0-time_temp))/(chain[i][2]/pembagi_waktu)+2-((chain[i][2]+chain[i][3])/(chain[i][2])))
        #print(time.process_time()-t_0)
        root.update()
        #time.sleep(1/25)
    move=False
    entry_page_variable.set(page_temp)
    entry_step_variable.set(step_temp)
        
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
            #print(i, j, chain[i][j][3])
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
                    sequence=sequence+frame_in_chain[i][l]+1
                
                #debug
                print(i, j, sequence, frame_in_chain[i][j])
                print(chain[i][sequence+frame_in_chain[i][j]][1])
                #print(chain[i][sequence+frame_in_chain[i][j]][2])
                #print(chain[i][sequence+frame_in_chain[i][j]][0])
                #print(chain[i][sequence-1][1])
                #print(chain[i][sequence-1][2])
                #print(chain[i][sequence-1][0])
                #print(page_step_rotasi[chain[i][sequence-1][1]][chain[i][sequence-1][2]][chain[i][sequence-1][0]], "+", ((k+1)/(frame_in_chain[i][j]+1))*(page_step_rotasi[chain[i][sequence+frame_in_chain[i][j]][1]][chain[i][sequence+frame_in_chain[i][j]][2]][chain[i][sequence+frame_in_chain[i][j]][0]]-page_step_rotasi[chain[i][sequence-1][1]][chain[i][sequence-1][2]][chain[i][sequence-1][0]]))
                #print(((k+1)/(frame_in_chain[i][j]+1)),"*(",page_step_rotasi[chain[i][sequence+frame_in_chain[i][j]][1]][chain[i][sequence+frame_in_chain[i][j]][2]][chain[i][sequence+frame_in_chain[i][j]][0]], "-", page_step_rotasi[chain[i][sequence-1][1]][chain[i][sequence-1][2]][chain[i][sequence-1][0]],")")
                
                if(page_step_rotasi[chain[i][sequence-1][1]][chain[i][sequence-1][2]][chain[i][sequence-1][0]+60]==0):
                    page_step_rotasi[chain[i][sequence+k][1]][chain[i][sequence+k][2]][chain[i][sequence+k][0]]=page_step_rotasi[chain[i][sequence-1][1]][chain[i][sequence-1][2]][chain[i][sequence-1][0]]+((k+1)/(frame_in_chain[i][j]+1))*(page_step_rotasi[chain[i][sequence+frame_in_chain[i][j]][1]][chain[i][sequence+frame_in_chain[i][j]][2]][chain[i][sequence+frame_in_chain[i][j]][0]]-page_step_rotasi[chain[i][sequence-1][1]][chain[i][sequence-1][2]][chain[i][sequence-1][0]])
                if(page_step_rotasi[chain[i][sequence-1][1]][chain[i][sequence-1][2]][chain[i][sequence-1][0]+60]==1):
                    page_step_rotasi[chain[i][sequence+k][1]][chain[i][sequence+k][2]][chain[i][sequence+k][0]]=page_step_rotasi[chain[i][sequence-1][1]][chain[i][sequence-1][2]][chain[i][sequence-1][0]]+(-math.cos(((k+1)/(frame_in_chain[i][j]+1))*(math.pi/2))+1)*(page_step_rotasi[chain[i][sequence+frame_in_chain[i][j]][1]][chain[i][sequence+frame_in_chain[i][j]][2]][chain[i][sequence+frame_in_chain[i][j]][0]]-page_step_rotasi[chain[i][sequence-1][1]][chain[i][sequence-1][2]][chain[i][sequence-1][0]])
                if(page_step_rotasi[chain[i][sequence-1][1]][chain[i][sequence-1][2]][chain[i][sequence-1][0]+60]==2):
                    page_step_rotasi[chain[i][sequence+k][1]][chain[i][sequence+k][2]][chain[i][sequence+k][0]]=page_step_rotasi[chain[i][sequence-1][1]][chain[i][sequence-1][2]][chain[i][sequence-1][0]]+(-math.cos(((k+1)/(frame_in_chain[i][j]+1))*(math.pi/2)+math.pi/2))*(page_step_rotasi[chain[i][sequence+frame_in_chain[i][j]][1]][chain[i][sequence+frame_in_chain[i][j]][2]][chain[i][sequence+frame_in_chain[i][j]][0]]-page_step_rotasi[chain[i][sequence-1][1]][chain[i][sequence-1][2]][chain[i][sequence-1][0]])
                if(page_step_rotasi[chain[i][sequence-1][1]][chain[i][sequence-1][2]][chain[i][sequence-1][0]+60]==3):
                    page_step_rotasi[chain[i][sequence+k][1]][chain[i][sequence+k][2]][chain[i][sequence+k][0]]=page_step_rotasi[chain[i][sequence-1][1]][chain[i][sequence-1][2]][chain[i][sequence-1][0]]+((-math.cos(((k+1)/(frame_in_chain[i][j]+1))*(math.pi))/2)+(1/2))*(page_step_rotasi[chain[i][sequence+frame_in_chain[i][j]][1]][chain[i][sequence+frame_in_chain[i][j]][2]][chain[i][sequence+frame_in_chain[i][j]][0]]-page_step_rotasi[chain[i][sequence-1][1]][chain[i][sequence-1][2]][chain[i][sequence-1][0]])

#transformation function
def transformation_0(kaki, pe, di, ur): #pentransformasi, ditrasformasi, urutan
    glTranslate(c.arana.part[kaki][pe].K_servo[0][0]+tx/20, c.arana.part[kaki][pe].K_servo[1][0]+ty/20, c.arana.part[kaki][pe].K_servo[2][0]-zpos)
    if(c.arana.part[kaki][pe].sumbu=="x"):
        if(c.arana.part[kaki][pe].arah_rotasi=="positif"):
            glRotatef(rotasi_servo[pe]+c.arana.part[kaki][pe].sudut_awal_rotasi,1,0,0)
        elif(c.arana.part[kaki][pe].arah_rotasi=="negatif"):
            glRotatef(-rotasi_servo[pe]+c.arana.part[kaki][pe].sudut_awal_rotasi,1,0,0)
    elif(c.arana.part[kaki][pe].sumbu=="y"):
        if(c.arana.part[kaki][pe].arah_rotasi=="positif"):
            glRotatef(rotasi_servo[pe]+c.arana.part[kaki][pe].sudut_awal_rotasi,0,1,0)
        elif(c.arana.part[kaki][pe].arah_rotasi=="negatif"):
            glRotatef(-rotasi_servo[pe]+c.arana.part[kaki][pe].sudut_awal_rotasi,0,1,0)
    elif(c.arana.part[kaki][pe].sumbu=="z"):
        if(c.arana.part[kaki][pe].arah_rotasi=="positif"):
            glRotatef(rotasi_servo[pe]+c.arana.part[kaki][pe].sudut_awal_rotasi,0,0,1)
        elif(c.arana.part[kaki][pe].arah_rotasi=="negatif"):
            glRotatef(-rotasi_servo[pe]+c.arana.part[kaki][pe].sudut_awal_rotasi,0,0,1)
    glTranslate(-c.arana.part[kaki][pe].K_servo[0][0]-tx/20, -c.arana.part[kaki][pe].K_servo[1][0]-ty/20, -c.arana.part[kaki][pe].K_servo[2][0]+zpos)
    if(pe!=di):
        transformation_0(kaki,c.arana.part[kaki][di].urutan_transformasi[ur+1],di,ur+1)

def transformation():
    for i in range(28):
        glLoadIdentity() #reset matix to identity matrix
        if(radio_button_kaki_napak_variable.get()==0):
            if(i==27):
                transformation_0("kiri",27,i,0)
            else:
                transformation_0("kiri",25,i,0)
        else:
            if(i==27):
                transformation_0("kanan",27,i,0)
            else:
                transformation_0("kanan",24,i,0)
        glTranslate(tx/20., ty/20., - zpos)
        glCallList(part[radio_button_kaki_napak_variable.get()][i].gl_list) #set part i to the transformed position in opengl
        
#Inverse kinematic function
def matriks_orientasi_part(id_part):
    matriks_temp=f.matriks_identitas()
    pe=id_part
    update_sudut_servo()
    while(pe!=-1):
        matriks_temp=np.dot(c.arana.part["kiri"][pe].M_rotasi, matriks_temp)
        pe=c.arana.part["kiri"][pe].parent
    return matriks_temp

def matriks_normal_part(id_part):
    matriks_temp=np.array([[0.], [0.], [0.]])
    a=matriks_orientasi_part(id_part)
    if(c.arana.part["kiri"][id_part].sumbu=="x"):
        b=0
    elif(c.arana.part["kiri"][id_part].sumbu=="y"):
        b=1
    elif(c.arana.part["kiri"][id_part].sumbu=="z"):
        b=2
    matriks_temp[0][0]=a[0][b]
    matriks_temp[1][0]=a[1][b]
    matriks_temp[2][0]=a[2][b]
    return matriks_temp
    
def project(N,V):
    return np.cross(N,(np.cross(V,N/np.linalg.norm(N), axis=0))/np.linalg.norm(N), axis=0)

def inverse(target_x, target_y, target_z, servo_1, servo_2, tolerance=10, max_iter=10):
    
    iteration=0
    distance=tolerance
    while(iteration<max_iter and distance>=tolerance):
        print("MSK LOOP")
        distance=ik(target_x, target_y, target_z, servo_1, servo_2)
        iteration=iteration+1
    print("DONE")
    '''
    #ccd method semi brute force
    d_theta=5
    iteration=1
    max_iteration=max_iter
    rotasi_servo_temp=[]
    minimal_dist=99999
    for i in range(27):
        rotasi_servo_temp.append(0)
    parent=servo_1
    dist=pow((pow(c.arana.part["kiri"][parent].KT_titik_berat[0][0]-target_x,2))+(pow(c.arana.part["kiri"][parent].KT_titik_berat[1][0]-target_y,2))+(pow(c.arana.part["kiri"][parent].KT_titik_berat[2][0]-target_z,2)),1/2)
    print(dist)
    while(dist>tolerance and iteration<max_iteration):
        parent=servo_1
        while(parent!=servo_2):
            clock.tick(25)
            for i in range(int(360/d_theta)):
                page_step_rotasi[int(entry_page.get())][int(entry_step.get())][parent]=(page_step_rotasi[int(entry_page.get())][int(entry_step.get())][parent]+d_theta)%360
                update_sudut_servo()
                f.transformasi(c.arana)
                dist=pow((pow(c.arana.part["kiri"][servo_1].KT_titik_berat[0][0]-target_x,2))+(pow(c.arana.part["kiri"][servo_1].KT_titik_berat[1][0]-target_y,2))+(pow(c.arana.part["kiri"][servo_1].KT_titik_berat[2][0]-target_z,2)),1/2)
                if(dist<minimal_dist):
                    rotasi_servo_temp[parent]=page_step_rotasi[int(entry_page.get())][int(entry_step.get())][parent]
                    minimal_dist=dist
                    draw()
                print(parent, page_step_rotasi[int(entry_page.get())][int(entry_step.get())][parent], rotasi_servo_temp[parent], minimal_dist, dist)
            page_step_rotasi[int(entry_page.get())][int(entry_step.get())][parent]=rotasi_servo_temp[parent]
            root.update()
            
            sphere = gluNewQuadric()
            glTranslate(0, 0, 0)
            glColor4f(0.5, 0.2, 0.2, 1) #Put color
            gluSphere(sphere, 1.0, 32, 16) #Draw sphere
            
            draw()
            parent=c.arana.part["kiri"][parent].parent
        iteration=iteration+1
        print(dist, iteration)
    '''

def ik(target_x, target_y, target_z, servo_1, servo_2):
    #page_step_rotasi[int(entry_page.get())][int(entry_step.get())][parent]
    A=np.array([[target_x],[target_y],[target_z]])
    V=np.array([[0.],[0.],[0.]])
    U=np.array([[0.],[0.],[0.]])
    n=c.arana.part["kiri"][servo_1].parent
#    print("servo_1", servo_1)
#    print("n", n)
    #dist_kecil=99999
    while(n!=c.arana.part["kiri"][servo_2].parent):
#        print("servo_1", servo_1)
#        print("n", n)
        update_sudut_servo()
        f.transformasi(c.arana)
        V=c.arana.part["kiri"][servo_1].KT_servo-c.arana.part["kiri"][n].KT_servo
#        print(c.arana.part["kiri"][servo_1].KT_servo)
#        print(c.arana.part["kiri"][n].KT_servo)
#        print("KT_servo_1", c.arana.part["kiri"][servo_1].KT_servo)
#        print("KT_servo_n", c.arana.part["kiri"][n].KT_servo)
        U=A-c.arana.part["kiri"][n].KT_servo
#        print("matriks normal part", matriks_normal_part(n))
        V_projected=project(matriks_normal_part(n), V)
        U_projected=project(matriks_normal_part(n), U)
        p=np.dot(np.transpose(U),V)/(np.linalg.norm(U)*np.linalg.norm(V))
#        print("U", U)
#        print("V", V)
#        print("P", p)
        #rint("V",V_projected,"U",U_projected)
#        if p<0:
#            tetha=-math.acos(p)
#        else:
        tetha=math.acos(p[0][0])
        if(type(tetha)!=type(1.0)):
            break
        print("TETHA", tetha)
        
        page_step_rotasi[int(entry_page.get())][int(entry_step.get())][n]=page_step_rotasi[int(entry_page.get())][int(entry_step.get())][n]+tetha*57.2958
        #print(page_step_rotasi[int(entry_page.get())][int(entry_step.get())][15])
        update_sudut_servo()
        f.transformasi(c.arana)
        
        dist_plus=pow(pow(A[0][0]-c.arana.part["kiri"][servo_1].KT_titik_berat[0][0], 2)+pow(A[1][0]-c.arana.part["kiri"][servo_1].KT_titik_berat[1][0], 2)+pow(A[2][0]-c.arana.part["kiri"][servo_1].KT_titik_berat[2][0], 2), 1/2)
        print("distance plus tetha", dist_plus)
        
        page_step_rotasi[int(entry_page.get())][int(entry_step.get())][n]=page_step_rotasi[int(entry_page.get())][int(entry_step.get())][n]-2*tetha*57.2958
        update_sudut_servo()
        f.transformasi(c.arana)
        
        dist_minus=pow(pow(A[0][0]-c.arana.part["kiri"][servo_1].KT_titik_berat[0][0], 2)+pow(A[1][0]-c.arana.part["kiri"][servo_1].KT_titik_berat[1][0], 2)+pow(A[2][0]-c.arana.part["kiri"][servo_1].KT_titik_berat[2][0], 2), 1/2)
        print("distance minus tetha",dist_minus)
        
        if(dist_minus>dist_plus):
            page_step_rotasi[int(entry_page.get())][int(entry_step.get())][n]=page_step_rotasi[int(entry_page.get())][int(entry_step.get())][n]+2*tetha*57.2958
#            if(dist_kecil>dist_plus):
#                dist_kecil=dist_plus
#            else:
#                page_step_rotasi[int(entry_page.get())][int(entry_step.get())][n]=page_step_rotasi[int(entry_page.get())][int(entry_step.get())][n]-tetha*57.2958
#        else:
#            if(dist_kecil>dist_minus):
#                dist_kecil=dist_minus
#            else:
#                page_step_rotasi[int(entry_page.get())][int(entry_step.get())][n]=page_step_rotasi[int(entry_page.get())][int(entry_step.get())][n]+tetha*57.2958
        update_sudut_servo()
        f.transformasi(c.arana)
        #print("dist_kecil", dist_kecil)
        
#        for i in range(27):
#            print("ROTASI", page_step_rotasi[int(entry_page.get())][int(entry_step.get())][i])
#        
        
#       print("matriks rotasi yang telah diupdate")
#        for i in (24,22,20,16):
#            print('Matrix rotasi:')
#            f.print_matriks(c.arana.part["kiri"][i].rotasi)
        n=c.arana.part["kiri"][n].parent
        draw()
        root.update()
    return pow(pow(A[0][0]-c.arana.part["kiri"][servo_1].KT_titik_berat[0][0], 2)+pow(A[1][0]-c.arana.part["kiri"][servo_1].KT_titik_berat[1][0], 2)+pow(A[2][0]-c.arana.part["kiri"][servo_1].KT_titik_berat[2][0], 2), 1/2)


#Inverse kinematic untuk napak
def ik_tapakin(target_x, target_z, rotasi_tapak):
    print(target_x, target_z, rotasi_tapak)
    
#draw to pygame opengl and tkinter canvas
def draw():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    canvas.delete("all")
    update_sudut_servo()
    f.transformasi(c.arana)
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
        line_L=canvas.create_line(c.arana.part["kiri"][28].KT_titik_berat[0][0]*scale+pos_x, c.arana.part["kiri"][28].KT_titik_berat[2][0]*scale+pos_z, c.arana.part["kiri"][29].KT_titik_berat[0][0]*scale+pos_x, c.arana.part["kiri"][29].KT_titik_berat[2][0]*scale+pos_z, c.arana.part["kiri"][30].KT_titik_berat[0][0]*scale+pos_x, c.arana.part["kiri"][30].KT_titik_berat[2][0]*scale+pos_z, c.arana.part["kiri"][31].KT_titik_berat[0][0]*scale+pos_x, c.arana.part["kiri"][31].KT_titik_berat[2][0]*scale+pos_z, c.arana.part["kiri"][28].KT_titik_berat[0][0]*scale+pos_x, c.arana.part["kiri"][28].KT_titik_berat[2][0]*scale+pos_z)
        circle_L=canvas.create_oval(f.titik_berat(c.arana, "kiri", "x")*scale+pos_x-rad, f.titik_berat(c.arana, "kiri", "z")*scale+pos_z-rad, f.titik_berat(c.arana, "kiri", "x")*scale+pos_x+rad, f.titik_berat(c.arana, "kiri", "z")*scale+pos_z+rad, fill=f._from_rgb((255,255,255)))
    else:
        rect_L=canvas.create_rectangle(0*scale+pos_x,0*scale+pos_z,-100*scale+pos_x,150*scale+pos_z)
        line_L=canvas.create_line(c.arana.part["kanan"][28].KT_titik_berat[0][0]*scale+pos_x, c.arana.part["kanan"][28].KT_titik_berat[2][0]*scale+pos_z, c.arana.part["kanan"][29].KT_titik_berat[0][0]*scale+pos_x, c.arana.part["kanan"][29].KT_titik_berat[2][0]*scale+pos_z, c.arana.part["kanan"][30].KT_titik_berat[0][0]*scale+pos_x, c.arana.part["kanan"][30].KT_titik_berat[2][0]*scale+pos_z, c.arana.part["kanan"][31].KT_titik_berat[0][0]*scale+pos_x, c.arana.part["kanan"][31].KT_titik_berat[2][0]*scale+pos_z, c.arana.part["kanan"][28].KT_titik_berat[0][0]*scale+pos_x, c.arana.part["kanan"][28].KT_titik_berat[2][0]*scale+pos_z)
        circle_L=canvas.create_oval(f.titik_berat(c.arana, "kanan", "x")*scale+pos_x-rad, f.titik_berat(c.arana, "kanan", "z")*scale+pos_z-rad, f.titik_berat(c.arana, "kanan", "x")*scale+pos_x+rad, f.titik_berat(c.arana, "kanan", "z")*scale+pos_z+rad, fill=f._from_rgb((255,255,255)))
    #for i in range(28):
    #    circle=canvas.create_oval(300/3+c.arana.part["kiri"][i].KT_titik_berat[0][0]*3/5,11*300/12-c.arana.part["kiri"][i].KT_titik_berat[1][0]*3/5,300/3+c.arana.part["kiri"][i].KT_titik_berat[0][0]*3/5+(c.arana.part["kiri"][i].KT_titik_berat[2][0]+300)/60,11*300/12-c.arana.part["kiri"][i].KT_titik_berat[1][0]*3/5+(c.arana.part["kiri"][i].KT_titik_berat[2][0]+300)/60, fill=f._from_rgb((255,255,255)))

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

button_copy_step=Button(frame_controller, text="copy step", command=lambda: copy_step())
button_copy_step.grid(row=7, column=2, sticky=W)

label_step=Label(frame_controller, text="step:")
label_step.grid(row=8, column=0)

entry_step_variable=IntVar()
entry_step=Entry(frame_controller, textvariable=entry_step_variable)
entry_step.grid(row=8, column=1)
entry_step_variable.set("0")

button_paste_step=Button(frame_controller, text="paste step", command=lambda: paste_step())
button_paste_step.grid(row=8, column=2, sticky=W)

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
entry_step_time_variable.set("40")

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

label_ik=Label(frame_controller, text="ik:")
label_ik.grid(row=18, column=0)

button_ik=Button(frame_controller, text="go", command=lambda:inverse(int(entry_posisi_tapak_x.get()), int(entry_posisi_tapak_y.get()), int(entry_posisi_tapak_z.get()),24,15))
button_ik.grid(row=18, column=1, sticky=W)

label_posisi_tapak_x=Label(frame_controller, text="posisi x:")
label_posisi_tapak_x.grid(row=19, column=0)

entry_posisi_tapak_x_variable=IntVar()
entry_posisi_tapak_x=Entry(frame_controller, textvariable=entry_posisi_tapak_x_variable)
entry_posisi_tapak_x.grid(row=19, column=1)
entry_posisi_tapak_x_variable.set("-110")

label_posisi_tapak_y=Label(frame_controller, text="posisi y:")
label_posisi_tapak_y.grid(row=20, column=0)

entry_posisi_tapak_y_variable=IntVar()
entry_posisi_tapak_y=Entry(frame_controller, textvariable=entry_posisi_tapak_y_variable)
entry_posisi_tapak_y.grid(row=20, column=1)
entry_posisi_tapak_y_variable.set("200")

label_posisi_tapak_z=Label(frame_controller, text="posisi z:")
label_posisi_tapak_z.grid(row=21, column=0)

entry_posisi_tapak_z_variable=IntVar()
entry_posisi_tapak_z=Entry(frame_controller, textvariable=entry_posisi_tapak_z_variable)
entry_posisi_tapak_z.grid(row=21, column=1)
entry_posisi_tapak_z_variable.set("300")

button_save_current_page=Button(frame_controller, text="save", command=lambda:save_all())
button_save_current_page.grid(row=22, column=0)

label_titik_berat=Label(frame_controller, text="ZMP(masih CoM):")
label_titik_berat.grid(row=23, column=0)

frame_canvas=Frame(root, width=350, height=250)
frame_canvas.grid(row=1, column=0)

canvas=Canvas(frame_canvas, width=400, height=200, bg=f._from_rgb((75,120,75)))
canvas.grid(row=0, column=0)

draw() #draw to pygame opengl and tkinter canvas for the first time

#looping pygame with pygame clock
while 1:
    clock.tick(25)
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
    