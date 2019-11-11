import csv

class Matriks:
    def __init__(self):
        self.banyak_baris=3
        self.banyak_kolom=3
        self.elemen=[[0,0,0],[0,0,0],[0,0,0]]
    
class Part:
    def __init__(self):
        self.koordinat_titik_berat_default=Matriks()
        self.koordinat_sumbu_rotasi_servo=Matriks()
        self.rotasi=Matriks()
        self.koordinat_titik_berat_tertransformasi=Matriks()
        self.parent=-1
        self.massa=0
        #self.model_3d_default=Matriks()
        #self.model_3d_tertransformasi=Matriks()
        self.urutan_transformasi=[]
        
    def load_data():
        n=0
        with open("data.csv","r") as data:
            data_reader=csv.reader(data)
        
            for line in data_reader:
                part[0][n].koordinat_titik_berat_default.banyak_baris=3
                part[0][n].koordinat_titik_berat_default.banyak_kolom=1
                part[0][n].koordinat_titik_berat_default.elemen[0][0]=float(line[0])
                part[0][n].koordinat_titik_berat_default.elemen[1][0]=float(line[1])
                part[0][n].koordinat_titik_berat_default.elemen[2][0]=float(line[2])
                part[0][n].koordinat_sumbu_rotasi_servo.banyak_baris=3
                part[0][n].koordinat_sumbu_rotasi_servo.banyak_kolom=1
                part[0][n].koordinat_sumbu_rotasi_servo.elemen[0][0]=float(line[3])
                part[0][n].koordinat_sumbu_rotasi_servo.elemen[1][0]=float(line[4])
                part[0][n].koordinat_sumbu_rotasi_servo.elemen[2][0]=float(line[5])
                part[0][n].parent=int(line[6])
                part[0][n].massa=float(line[7])
                part[1][n].koordinat_titik_berat_default.banyak_baris=3
                part[1][n].koordinat_titik_berat_default.banyak_kolom=1
                part[1][n].koordinat_titik_berat_default.elemen[0][0]=float(line[8])
                part[1][n].koordinat_titik_berat_default.elemen[1][0]=float(line[9])
                part[1][n].koordinat_titik_berat_default.elemen[2][0]=float(line[10])
                part[1][n].koordinat_sumbu_rotasi_servo.banyak_baris=3
                part[1][n].koordinat_sumbu_rotasi_servo.banyak_kolom=1
                part[1][n].koordinat_sumbu_rotasi_servo.elemen[0][0]=float(line[11])
                part[1][n].koordinat_sumbu_rotasi_servo.elemen[1][0]=float(line[12])
                part[1][n].koordinat_sumbu_rotasi_servo.elemen[2][0]=float(line[13])
                part[1][n].parent=int(line[14])
                part[1][n].massa=float(line[15])
                n=n+1

    
part=[[],[]]
for i in range(31):
    part[0].append(Part())
    part[1].append(Part())
    
part[0][0].urutan_transformasi=[25,23,21,17,19,15,13,26,2,0]
part[0][1].urutan_transformasi=[25,23,21,17,19,15,13,26,2,0,1]
part[0][2].urutan_transformasi=[25,23,21,17,19,15,13,26,2]
part[0][3].urutan_transformasi=[25,23,21,17,19,15,13,26,3]
part[0][4].urutan_transformasi=[25,23,21,17,19,15,13,26,4]
part[0][5].urutan_transformasi=[25,23,21,17,19,15,13,26,3,5]
part[0][6].urutan_transformasi=[25,23,21,17,19,15,13,26,4,6]
part[0][7].urutan_transformasi=[25,23,21,17,19,15,13,26,3,5,7]
part[0][8].urutan_transformasi=[25,23,21,17,19,15,13,26,4,6,8]
part[0][9].urutan_transformasi=[25,23,21,17,19,15,13,26,3,5,7,9]
part[0][10].urutan_transformasi=[25,23,21,17,19,15,13,26,4,6,8,10]
part[0][11].urutan_transformasi=[25,23,21,17,19,15,13,26,3,5,7,9,11]
part[0][12].urutan_transformasi=[25,23,21,17,19,15,13,26,4,6,8,10,12]
part[0][13].urutan_transformasi=[25,23,21,17,19,15,13]
part[0][14].urutan_transformasi=[25,23,21,17,19,15,14]
part[0][15].urutan_transformasi=[25,23,21,17,19,15]
part[0][16].urutan_transformasi=[25,23,21,17,19,15,14,18,16]
part[0][17].urutan_transformasi=[25,23,21,17]
part[0][18].urutan_transformasi=[25,23,21,17,19,15,14,18]
part[0][19].urutan_transformasi=[25,23,21,17,19]
part[0][20].urutan_transformasi=[25,23,21,17,19,15,14,18,16,20]
part[0][21].urutan_transformasi=[25,23,21]
part[0][22].urutan_transformasi=[25,23,21,17,19,15,14,18,16,20,22]
part[0][23].urutan_transformasi=[25,23]
part[0][24].urutan_transformasi=[25,23,21,17,19,15,14,18,16,20,22,24]
part[0][25].urutan_transformasi=[25]
part[0][26].urutan_transformasi=[25,23,21,17,19,15,13,26]
'''
part[1].append(25,23,21,17,19,15,13,26,2,0)
part[2].append(25,23,21,17,19,15,13,26,2)'''

    