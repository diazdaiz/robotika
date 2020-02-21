import numpy as np
import json

class Robot:
    def __init__(self, banyak_part, data_part):
        self.banyak_part=banyak_part+5 #ada part tambahan untuk obj telapak kaki pyopengl dan titik pembuat polygon untuk area zmp
        self.data_part=data_part
        self.part={"kiri":[], "kanan":[]} #part dibagi berdasarkan 2 koordinat, part dengan koordinat kaki kiri dan kanan
        for id_part in range(self.banyak_part):
            self.part["kiri"].append(Part())
            self.part["kanan"].append(Part())
                
    def load_part(self):
        with open(self.data_part) as f:
            data=json.load(f)
            for i in range(len(data)):
                self.part[data[i]["kaki"]][int(data[i]["id"])].kaki=data[i]["kaki"]
                self.part[data[i]["kaki"]][int(data[i]["id"])].id=data[i]["id"]
                self.part[data[i]["kaki"]][int(data[i]["id"])].K_titik_berat=np.array(data[i]["K_titik_berat"])
                self.part[data[i]["kaki"]][int(data[i]["id"])].K_servo=np.array(data[i]["K_servo"])
                self.part[data[i]["kaki"]][int(data[i]["id"])].sumbu=data[i]["sumbu"]
                self.part[data[i]["kaki"]][int(data[i]["id"])].arah_rotasi=data[i]["arah_rotasi"]
                self.part[data[i]["kaki"]][int(data[i]["id"])].sudut_awal_rotasi=data[i]["sudut_awal_rotasi"]
                self.part[data[i]["kaki"]][int(data[i]["id"])].parent=data[i]["parent"]
                self.part[data[i]["kaki"]][int(data[i]["id"])].massa=data[i]["massa"]
                self.part[data[i]["kaki"]][int(data[i]["id"])].model=data[i]["model"]
                self.part[data[i]["kaki"]][int(data[i]["id"])].urutan_transformasi=data[i]["urutan_transformasi"]
                self.part[data[i]["kaki"]][int(data[i]["id"])].keterangan_tambahan=data[i]["keterangan_tambahan"]
    
    def save_part(self):
        a=[]
        for i in range(32):
            a.append(self.part["kiri"][i].to_dict())
        for i in range(32):
            a.append(self.part["kanan"][i].to_dict())
        with open("data/data.json", "w") as f:
            json.dump(a, f, indent=2)

class Part:
    def __init__(self):
        self.kaki="kiri" #/kanan, koordinat partnya berdasarkan kaki kiri/kanan
        self.id=0 #id part
        self.K_titik_berat=np.array([[0.],[0.],[0.]]) #koordinat titik berat
        self.KT_titik_berat=np.array([[0.],[0.],[0.]]) #koordinat tertransformasi dari titik berat
        self.K_servo=np.array([[0.],[0.],[0.]]) #koordinat titik rotasi servo
        self.KT_servo=np.array([[0.],[0.],[0.]]) #koordinat tertransformasi dari titik rotasi servo 
        self.sumbu="x" #/y/z, sumbu rotasi servo saat tidak tertransformasi
        self.arah_rotasi="positif" #arah rotasi servo
        self.sudut_awal_rotasi=0 #sudut awal rotasi servo
        self.M_rotasi=np.array([[0.,0.,0.],[0.,0.,0.],[0.,0.,0.]]) #matriks rotasi servo
        self.parent=-1 #parent dari part (-1=tidak mempunya parent)
        self.massa=0 #massa dari part
        self.model="none" #3d model dari part
        self.urutan_transformasi=[] #untuk urutan transformasi pyopengl
        self.keterangan_tambahan="none"

    def to_dict(self): #yang perlu disave pada data.json dibuat menjadi dictionary terlebih dahulu
        return ({
                "kaki" : self.kaki, 
                "id" : self.id, 
                "K_titik_berat" : self.K_titik_berat.tolist(), 
                "K_servo" : self.K_servo.tolist(), 
                "sumbu" : self.sumbu,
                "arah_rotasi" : self.arah_rotasi,
                "sudut_awal_rotasi" : self.sudut_awal_rotasi,
                "parent" : self.parent, 
                "massa" : self.massa,
                "model" : self.model,
                "urutan_transformasi" : self.urutan_transformasi,
                "keterangan_tambahan" : self.keterangan_tambahan}) 
    
arana=Robot(27, "data/data.json")
arana.load_part()
#arana.part["kiri"][4].arah_rotasi="negatif"
#arana.part["kiri"][5].arah_rotasi="negatif"
#arana.part["kiri"][6].arah_rotasi="negatif"
#arana.part["kiri"][8].arah_rotasi="negatif"
#arana.part["kiri"][12].arah_rotasi="negatif"
#arana.part["kiri"][14].arah_rotasi="negatif"
#arana.part["kiri"][16].arah_rotasi="negatif"
#arana.part["kiri"][17].arah_rotasi="negatif"
#arana.part["kiri"][18].arah_rotasi="negatif"
#arana.part["kiri"][20].arah_rotasi="negatif"
#arana.part["kiri"][21].arah_rotasi="negatif"
#arana.part["kiri"][25].arah_rotasi="negatif"
#
#arana.part["kanan"][4].arah_rotasi="negatif"
#arana.part["kanan"][5].arah_rotasi="negatif"
#arana.part["kanan"][6].arah_rotasi="negatif"
#arana.part["kanan"][8].arah_rotasi="negatif"
#arana.part["kanan"][12].arah_rotasi="negatif"
#arana.part["kanan"][15].arah_rotasi="negatif"
#arana.part["kanan"][19].arah_rotasi="negatif"
#arana.part["kanan"][22].arah_rotasi="negatif"
#arana.part["kanan"][23].arah_rotasi="negatif"
#arana.part["kanan"][24].arah_rotasi="negatif"
#
#arana.part["kiri"][3].sudut_awal_rotasi=-90.
#arana.part["kiri"][4].sudut_awal_rotasi=-90.
#arana.part["kiri"][5].sudut_awal_rotasi=-90.
#arana.part["kiri"][6].sudut_awal_rotasi=90.
#arana.part["kiri"][7].sudut_awal_rotasi=90.
#arana.part["kiri"][8].sudut_awal_rotasi=90.
#
#arana.part["kanan"][3].sudut_awal_rotasi=-90.
#arana.part["kanan"][4].sudut_awal_rotasi=-90.
#arana.part["kanan"][5].sudut_awal_rotasi=-90.
#arana.part["kanan"][6].sudut_awal_rotasi=90.
#arana.part["kanan"][7].sudut_awal_rotasi=90.
#arana.part["kanan"][8].sudut_awal_rotasi=90.
#arana.part["kanan"][9].sudut_awal_rotasi=0
#
arana.save_part()