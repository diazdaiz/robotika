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
    
part=[[],[]]
for i in range(31):
    part[0].append(Part())
    part[1].append(Part())