import Class as c
import numpy as np
import math
            
#membuat matriks khusus
def matriks_rotasi(sumbu, sudut, arah_rotasi, sudut_awal_rotasi):
    if(sumbu=="x"):
        sumbu=0
    elif(sumbu=="y"):
        sumbu=1
    elif(sumbu=="z"):
        sumbu=2
    if(arah_rotasi=="positif"):
        sudut=(sudut+sudut_awal_rotasi)*math.pi/180
    elif(arah_rotasi=="negatif"):
        sudut=-(sudut+sudut_awal_rotasi)*math.pi/180
    mtemp=np.array([[0., 0., 0.],[0., 0., 0.],[0., 0., 0.]])
    mtemp[sumbu][sumbu]=1;
    n=0
    for i in range(2):
        for j in range(2):
            if(n==0):
                mtemp[(sumbu+i+1)%3][(sumbu+j+1)%3]=math.cos(sudut)
            if(n==1):
                mtemp[(sumbu+i+1)%3][(sumbu+j+1)%3]=-math.sin(sudut)
            if(n==2):
                mtemp[(sumbu+i+1)%3][(sumbu+j+1)%3]=math.sin(sudut)
            if(n==3):
                mtemp[(sumbu+i+1)%3][(sumbu+j+1)%3]=math.cos(sudut)
            n=n+1
    return mtemp

def matriks_identitas(): #3x3
    return np.array([[1., 0., 0.],[0., 1., 0.],[0., 0., 1.]])

#transformasi
def transformasi(robot): #transformasi koordinat titik berat dan titik rotasi servo 
    for id_part in range(32):
        #berdasarkan kaki kiri
        #transformasi titik berat
        pe=id_part #pentransformasi
        robot.part["kiri"][id_part].KT_titik_berat=robot.part["kiri"][pe].K_titik_berat-robot.part["kiri"][pe].K_servo
        robot.part["kiri"][id_part].KT_titik_berat=np.dot(robot.part["kiri"][pe].M_rotasi, robot.part["kiri"][id_part].KT_titik_berat)
        robot.part["kiri"][id_part].KT_titik_berat+=robot.part["kiri"][pe].K_servo
        pe=robot.part["kiri"][pe].parent
        while(pe!=-1):
            robot.part["kiri"][id_part].KT_titik_berat-=robot.part["kiri"][pe].K_servo
            robot.part["kiri"][id_part].KT_titik_berat=np.dot(robot.part["kiri"][pe].M_rotasi, robot.part["kiri"][id_part].KT_titik_berat)
            robot.part["kiri"][id_part].KT_titik_berat+=robot.part["kiri"][pe].K_servo
            pe=robot.part["kiri"][pe].parent
        #transformasi titik rotasi servo
        pe=id_part #pentransformasi
        robot.part["kiri"][id_part].KT_servo=robot.part["kiri"][pe].K_servo-robot.part["kiri"][pe].K_servo
        robot.part["kiri"][id_part].KT_servo=np.dot(robot.part["kiri"][pe].M_rotasi, robot.part["kiri"][id_part].KT_servo)
        robot.part["kiri"][id_part].KT_servo+=robot.part["kiri"][pe].K_servo
        pe=robot.part["kiri"][pe].parent
        while(pe!=-1):
            robot.part["kiri"][id_part].KT_servo-=robot.part["kiri"][pe].K_servo
#            print("Kurang", robot.part["kiri"][id_part].KT_servo)
            robot.part["kiri"][id_part].KT_servo=np.dot(robot.part["kiri"][pe].M_rotasi, robot.part["kiri"][id_part].KT_servo)
            
#            print("Kali", robot.part["kiri"][id_part].KT_servo)
            robot.part["kiri"][id_part].KT_servo+=robot.part["kiri"][pe].K_servo
#            print("Tambah", robot.part["kiri"][id_part].KT_servo)
            pe=robot.part["kiri"][pe].parent
        #print(id_part, robot.part["kiri"][id_part].KT_servo)
        
        #berdasarkan kaki kanan
        #transformasi titik berat
        pe=id_part #pentransformasi
        robot.part["kanan"][id_part].KT_titik_berat=robot.part["kanan"][pe].K_titik_berat-robot.part["kanan"][pe].K_servo
        robot.part["kanan"][id_part].KT_titik_berat=np.dot(robot.part["kanan"][pe].M_rotasi, robot.part["kanan"][id_part].KT_titik_berat)
        robot.part["kanan"][id_part].KT_titik_berat+=robot.part["kanan"][pe].K_servo
        pe=robot.part["kanan"][pe].parent
        while(pe!=-1):
            robot.part["kanan"][id_part].KT_titik_berat-=robot.part["kanan"][pe].K_servo
            robot.part["kanan"][id_part].KT_titik_berat=np.dot(robot.part["kanan"][pe].M_rotasi, robot.part["kanan"][id_part].KT_titik_berat)
            robot.part["kanan"][id_part].KT_titik_berat+=robot.part["kanan"][pe].K_servo
            pe=robot.part["kanan"][pe].parent
        #transformasi titik rotasi servo
        pe=id_part #pentransformasi
        robot.part["kanan"][id_part].KT_servo=robot.part["kanan"][pe].K_titik_berat-robot.part["kanan"][pe].K_servo
        robot.part["kanan"][id_part].KT_servo=np.dot(robot.part["kanan"][pe].M_rotasi, robot.part["kanan"][id_part].KT_servo)
        robot.part["kanan"][id_part].KT_servo+=robot.part["kanan"][pe].K_servo
        pe=robot.part["kanan"][pe].parent
        while(pe!=-1):
            robot.part["kanan"][id_part].KT_servo-=robot.part["kanan"][pe].K_servo
            robot.part["kanan"][id_part].KT_servo=np.dot(robot.part["kanan"][pe].M_rotasi, robot.part["kanan"][id_part].KT_servo)
            robot.part["kanan"][id_part].KT_servo+=robot.part["kanan"][pe].K_servo
            pe=robot.part["kanan"][pe].parent
        

#Penghitung titik berat
def titik_berat(robot, kaki, sumbu):
    if(sumbu=="x"):
        sumbu=0
    elif(sumbu=="y"):
        sumbu=1
    elif(sumbu=="z"):
        sumbu=2
    m=0
    t=0
    for i in range(28):
        m=m+robot.part[kaki][i].massa
        t=t+robot.part[kaki][i].KT_titik_berat[sumbu][0]*robot.part[kaki][i].massa
    return t/m

"""https://stackoverflow.com/questions/51591456/can-i-use-rgb-in-tkinter"""
def _from_rgb(rgb): 
    return "#%02x%02x%02x" % rgb  