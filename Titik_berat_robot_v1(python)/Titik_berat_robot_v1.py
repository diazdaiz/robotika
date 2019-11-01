import Fungsi as f
import Class as c
import Graphics as g

#load data
f.load(c.part)

#update sudut rotasi servo tiap saat(belum)
c.part[0][0].rotasi=f.matriks_rotasi(0,0);
c.part[0][1].rotasi=f.matriks_rotasi(2,0);
c.part[0][2].rotasi=f.matriks_rotasi(1,0);
c.part[0][3].rotasi=f.matriks_rotasi(0,0);
c.part[0][4].rotasi=f.matriks_rotasi(0,0);
c.part[0][5].rotasi=f.matriks_rotasi(2,0);
c.part[0][6].rotasi=f.matriks_rotasi(2,0);
c.part[0][7].rotasi=f.matriks_rotasi(1,0);
c.part[0][8].rotasi=f.matriks_rotasi(1,0);
c.part[0][9].rotasi=f.matriks_rotasi(0,0);
c.part[0][10].rotasi=f.matriks_rotasi(0,0);
c.part[0][11].rotasi=f.matriks_rotasi(2,0);
c.part[0][12].rotasi=f.matriks_rotasi(2,0);
c.part[0][13].rotasi=f.matriks_rotasi(1,0);
c.part[0][14].rotasi=f.matriks_rotasi(1,0);
c.part[0][15].rotasi=f.matriks_rotasi(1,0);
c.part[0][16].rotasi=f.matriks_rotasi(0,30);
c.part[0][17].rotasi=f.matriks_rotasi(0,0);
c.part[0][18].rotasi=f.matriks_rotasi(2,0);
c.part[0][19].rotasi=f.matriks_rotasi(2,60);
c.part[0][20].rotasi=f.matriks_rotasi(0,0);
c.part[0][21].rotasi=f.matriks_rotasi(0,0);
c.part[0][22].rotasi=f.matriks_rotasi(0,0);
c.part[0][23].rotasi=f.matriks_rotasi(0,0);
c.part[0][24].rotasi=f.matriks_rotasi(2,0);
c.part[0][25].rotasi=f.matriks_rotasi(2,0);
c.part[0][26].rotasi=f.matriks_rotasi(2,-30);
c.part[0][27].rotasi=f.matriks_identitas();
c.part[0][28].rotasi=f.matriks_identitas();
c.part[0][29].rotasi=f.matriks_identitas();
c.part[0][30].rotasi=f.matriks_identitas();
  
c.part[1][0].rotasi=f.matriks_rotasi(0,0);
c.part[1][1].rotasi=f.matriks_rotasi(2,0);
c.part[1][2].rotasi=f.matriks_rotasi(1,0);
c.part[1][3].rotasi=f.matriks_rotasi(0,0);
c.part[1][4].rotasi=f.matriks_rotasi(0,0);
c.part[1][5].rotasi=f.matriks_rotasi(2,0);
c.part[1][6].rotasi=f.matriks_rotasi(2,0);
c.part[1][7].rotasi=f.matriks_rotasi(1,0);
c.part[1][8].rotasi=f.matriks_rotasi(1,0);
c.part[1][9].rotasi=f.matriks_rotasi(0,0);
c.part[1][10].rotasi=f.matriks_rotasi(0,0);
c.part[1][11].rotasi=f.matriks_rotasi(2,0);
c.part[1][12].rotasi=f.matriks_rotasi(2,0);
c.part[1][13].rotasi=f.matriks_rotasi(1,0);
c.part[1][14].rotasi=f.matriks_rotasi(1,0);
c.part[1][15].rotasi=f.matriks_rotasi(1,0);
c.part[1][16].rotasi=f.matriks_rotasi(0,0);
c.part[1][17].rotasi=f.matriks_rotasi(0,0);
c.part[1][18].rotasi=f.matriks_rotasi(2,0);
c.part[1][19].rotasi=f.matriks_rotasi(2,-60);
c.part[1][20].rotasi=f.matriks_rotasi(0,0);
c.part[1][21].rotasi=f.matriks_rotasi(0,0);
c.part[1][22].rotasi=f.matriks_rotasi(0,0);
c.part[1][23].rotasi=f.matriks_rotasi(0,0);
c.part[1][24].rotasi=f.matriks_rotasi(2,0);
c.part[1][25].rotasi=f.matriks_rotasi(2,0);
c.part[1][26].rotasi=f.matriks_rotasi(2,0);
c.part[1][27].rotasi=f.matriks_identitas();
c.part[1][28].rotasi=f.matriks_identitas();
c.part[1][29].rotasi=f.matriks_identitas();
c.part[1][30].rotasi=f.matriks_identitas();

f.transformasi(c.part)

#gambar
win_width=1000
win_height=600
def main():
    win=g.GraphWin("Titik_berat_robot_v1", win_width, win_height)
    win.setBackground(g.color_rgb(75,120,75))
    
    #titik-titik berat tertransformasi
    for i in range(27):
        #hanyak kaki kiri/kedua kaki yang menapak
        pt=g.Point(win_width/4+c.part[0][i].koordinat_titik_berat_tertransformasi.elemen[0][0]*2/5,11*win_height/12-c.part[0][i].koordinat_titik_berat_tertransformasi.elemen[1][0]*2/5)
        cir=g.Circle(pt,4)
        cir.setFill(g.color_rgb(255,255,255))
        cir.draw(win)
        
        #hanya kaki kanan yang menapak
        pt=g.Point(3*win_width/4+c.part[1][i].koordinat_titik_berat_tertransformasi.elemen[0][0]*2/5,11*win_height/12-c.part[1][i].koordinat_titik_berat_tertransformasi.elemen[1][0]*2/5)
        cir=g.Circle(pt,4)
        cir.setFill(g.color_rgb(255,255,255))
        cir.draw(win)
        
    #area dimana titik berat harus berada
    #telapak kaki kiri berdasarkan koordinat (0,0,0) di telapak kaki kiri bagian kiri belakang
    poly=g.Polygon(g.Point(win_width/8,2*win_height/5),g.Point(win_width/8+100,2*win_height/5),g.Point(win_width/8+100,2*win_height/5-150),g.Point(win_width/8,2*win_height/5-150))
    poly.setFill(g.color_rgb(75,120,75))
    poly.draw(win)
    
    #telapak kaki kanan berdasarkan koordinat (0,0,0) di telapak kaki kiri bagian kiri belakang
    poly=g.Polygon(g.Point(win_width/8+c.part[0][27].koordinat_titik_berat_tertransformasi.elemen[0][0],2*win_height/5-c.part[0][27].koordinat_titik_berat_tertransformasi.elemen[2][0]),g.Point(win_width/8+c.part[0][28].koordinat_titik_berat_tertransformasi.elemen[0][0],2*win_height/5-c.part[0][28].koordinat_titik_berat_tertransformasi.elemen[2][0]),g.Point(win_width/8+c.part[0][29].koordinat_titik_berat_tertransformasi.elemen[0][0],2*win_height/5-c.part[0][29].koordinat_titik_berat_tertransformasi.elemen[2][0]),g.Point(win_width/8+c.part[0][30].koordinat_titik_berat_tertransformasi.elemen[0][0],2*win_height/5-c.part[0][30].koordinat_titik_berat_tertransformasi.elemen[2][0]))
    poly.setFill(g.color_rgb(75,120,75))
    poly.draw(win)
    
    #titik berat berdasarkan koordinat (0,0,0) di telapak kaki kiri bagian kiri belakang
    pt=g.Point(win_width/8+f.titik_berat_x_L(c.part),2*win_height/5-f.titik_berat_z_L(c.part))
    cir=g.Circle(pt,15)
    cir.setFill(g.color_rgb(255,255,255))
    cir.draw(win)
    
    #telapak kaki kanan berdasarkan koordinat (0,0,0) di telapak kaki kanan bagian kiri belakang
    poly=g.Polygon(g.Point(6*win_width/8,2*win_height/5),g.Point(6*win_width/8+100,2*win_height/5),g.Point(6*win_width/8+100,2*win_height/5-150),g.Point(6*win_width/8,2*win_height/5-150))
    poly.setFill(g.color_rgb(75,120,75))
    poly.draw(win)
    
    #titik berat berdasarkan koordinat (0,0,0) di telapak kaki kiri bagian kiri belakang
    pt=g.Point(6*win_width/8+f.titik_berat_x_R(c.part),2*win_height/5-f.titik_berat_z_R(c.part))
    cir=g.Circle(pt,15)
    cir.setFill(g.color_rgb(255,255,255))
    cir.draw(win)
    
    win.getMouse()
    win.close()
    
main()
