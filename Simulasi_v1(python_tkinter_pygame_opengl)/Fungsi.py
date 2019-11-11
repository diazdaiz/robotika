import Class as c
import math
            
#print matriks
def print_matriks(m1=c.Matriks()):
    for i in range(m1.banyak_baris):
        for j in range(m1.banyak_kolom):
            print(m1.elemen[i][j])

#operasi matriks
def tambah(m1,m2,m3):
    mtemp=[[0,0,0],[0,0,0],[0,0,0]]
    m3.banyak_baris=m1.banyak_baris
    m3.banyak_kolom=m1.banyak_kolom
    for i in range(m3.banyak_baris):
        for j in range(m3.banyak_kolom):
            mtemp[i][j]=m1.elemen[i][j]+m2.elemen[i][j]
    for i in range(m3.banyak_baris):
        for j in range(m3.banyak_kolom):
            m3.elemen[i][j]=mtemp[i][j]
            
def kurang(m1,m2,m3):
    mtemp=[[0,0,0],[0,0,0],[0,0,0]]
    m3.banyak_baris=m1.banyak_baris
    m3.banyak_kolom=m1.banyak_kolom
    for i in range(m3.banyak_baris):
        for j in range(m3.banyak_kolom):
            mtemp[i][j]=m1.elemen[i][j]-m2.elemen[i][j]
    for i in range(m3.banyak_baris):
        for j in range(m3.banyak_kolom):
            m3.elemen[i][j]=mtemp[i][j]

def kali(m1,m2,m3):
    mtemp=[[0,0,0],[0,0,0],[0,0,0]]
    m3.banyak_baris=m1.banyak_baris
    m3.banyak_kolom=m2.banyak_kolom
    for i in range(m1.banyak_baris):
        for j in range(m2.banyak_kolom):
            x=0
            for k in range(m1.banyak_kolom):
                x=x+(m1.elemen[i][k]*m2.elemen[k][j]);
            mtemp[i][j]=x;
    for i in range(m3.banyak_baris):
        for j in range(m3.banyak_kolom):
            m3.elemen[i][j]=mtemp[i][j]

#membuat matriks khusus
def matriks_rotasi(sumbu, sudut): #0x,1y,2z
    mtemp=c.Matriks()
    sudut=sudut*math.pi/180;
    mtemp.banyak_baris=3;
    mtemp.banyak_kolom=3;
    for i in range(3):
        for j in range(3):
            mtemp.elemen[i][j]=0
    n=0
    mtemp.elemen[sumbu][sumbu]=1;
    for i in range(2):
        for j in range(2):
            if(n==0):
                mtemp.elemen[(sumbu+i+1)%3][(sumbu+j+1)%3]=math.cos(sudut)
            if(n==1):
                mtemp.elemen[(sumbu+i+1)%3][(sumbu+j+1)%3]=-math.sin(sudut)
            if(n==2):
                mtemp.elemen[(sumbu+i+1)%3][(sumbu+j+1)%3]=math.sin(sudut)
            if(n==3):
                mtemp.elemen[(sumbu+i+1)%3][(sumbu+j+1)%3]=math.cos(sudut)
            n=n+1
    return mtemp

def matriks_identitas():
    mtemp=c.Matriks()
    mtemp.elemen[0][0]=1
    mtemp.elemen[1][1]=1
    mtemp.elemen[2][2]=1
    return mtemp

#transformasi
def transformasi_0(part):
    kurang(part.koordinat_titik_berat_default, part.koordinat_sumbu_rotasi_servo, part.koordinat_titik_berat_tertransformasi)
    kali(part.rotasi, part.koordinat_titik_berat_tertransformasi, part.koordinat_titik_berat_tertransformasi)
    tambah(part.koordinat_titik_berat_tertransformasi, part.koordinat_sumbu_rotasi_servo, part.koordinat_titik_berat_tertransformasi)

def transformasi_1(part, kaki, pe, di): #pentransformasi, ditransformasi
    kurang(part[kaki][di].koordinat_titik_berat_tertransformasi, part[kaki][pe].koordinat_sumbu_rotasi_servo, part[kaki][di].koordinat_titik_berat_tertransformasi)
    kali(part[kaki][pe].rotasi, part[kaki][di].koordinat_titik_berat_tertransformasi, part[kaki][di].koordinat_titik_berat_tertransformasi)
    tambah(part[kaki][di].koordinat_titik_berat_tertransformasi, part[kaki][pe].koordinat_sumbu_rotasi_servo, part[kaki][di].koordinat_titik_berat_tertransformasi)
    if(part[kaki][pe].parent!=-1):
        transformasi_1(part, kaki, part[kaki][pe].parent, di)

def transformasi(part):
    for i in range(31):
        #kaki kiri
        transformasi_0(part[0][i])
        if(part[0][i].parent!=-1):
            transformasi_1(part, 0, part[0][i].parent, i)
        #kaki kanan
        transformasi_0(part[1][i])
        if(part[1][i].parent!=-1):
            transformasi_1(part, 1, part[1][i].parent, i)

#Penghitung titik berat
def massa_total(part):
    m=0
    for i in range(27):
        m=m+part[0][i].massa
    return m

def titik_berat_x_L(part):
    t=0
    for i in range(27):
        t=t+part[0][i].koordinat_titik_berat_tertransformasi.elemen[0][0]*part[0][i].massa
    t=(t+104.98*52.05)/(massa_total(part)+104.98)
    return t

def titik_berat_z_L(part):
    t=0;
    for i in range(27):
        t=t+part[0][i].koordinat_titik_berat_tertransformasi.elemen[2][0]*part[0][i].massa
    t=(t+104.98*75.27)/(massa_total(part)+104.98)
    return t

def titik_berat_x_R(part):
    t=0;
    for i in range(27):
        t=t+part[1][i].koordinat_titik_berat_tertransformasi.elemen[0][0]*part[1][i].massa
    t=(t+104.98*47.16)/(massa_total(part)+104.98)
    return t

def titik_berat_z_R(part):
    t=0;
    for i in range(27):
        t=t+part[1][i].koordinat_titik_berat_tertransformasi.elemen[2][0]*part[1][i].massa
    t=(t+104.98*75.23)/(massa_total(part)+104.98)
    return t

"""https://stackoverflow.com/questions/51591456/can-i-use-rgb-in-tkinter"""
def _from_rgb(rgb): 
    return "#%02x%02x%02x" % rgb  