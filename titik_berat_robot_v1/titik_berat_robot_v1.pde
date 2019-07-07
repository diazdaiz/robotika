Part[][] part=new Part[2][31]; //index di kiri(0=kaki kiri, 1=kaki kanan).index di kanan(0-26=servo, 27-30=titik tambahan)

void setup(){
  size(1000,600);
  background(75,120,75);
  for(int i=0; i<31; i++){
    part[0][i]=new Part();
    part[1][i]=new Part();
  }
  load(part);
}

void draw(){
  //update sudut rotasi servo tiap saat(belum)
  part[0][0].rotasi=matriks_rotasi(0,0);
  part[0][1].rotasi=matriks_rotasi(2,0);
  part[0][2].rotasi=matriks_rotasi(1,0);
  part[0][3].rotasi=matriks_rotasi(0,0);
  part[0][4].rotasi=matriks_rotasi(0,0);
  part[0][5].rotasi=matriks_rotasi(2,0);
  part[0][6].rotasi=matriks_rotasi(2,0);
  part[0][7].rotasi=matriks_rotasi(1,0);
  part[0][8].rotasi=matriks_rotasi(1,0);
  part[0][9].rotasi=matriks_rotasi(0,0);
  part[0][10].rotasi=matriks_rotasi(0,0);
  part[0][11].rotasi=matriks_rotasi(2,0);
  part[0][12].rotasi=matriks_rotasi(2,0);
  part[0][13].rotasi=matriks_rotasi(1,0);
  part[0][14].rotasi=matriks_rotasi(1,0);
  part[0][15].rotasi=matriks_rotasi(1,0);
  part[0][16].rotasi=matriks_rotasi(0,0);
  part[0][17].rotasi=matriks_rotasi(0,0);
  part[0][18].rotasi=matriks_rotasi(2,0);
  part[0][19].rotasi=matriks_rotasi(2,60);
  part[0][20].rotasi=matriks_rotasi(0,0);
  part[0][21].rotasi=matriks_rotasi(0,0);
  part[0][22].rotasi=matriks_rotasi(0,0);
  part[0][23].rotasi=matriks_rotasi(0,0);
  part[0][24].rotasi=matriks_rotasi(2,0);
  part[0][25].rotasi=matriks_rotasi(2,0);
  part[0][26].rotasi=matriks_rotasi(2,0);
  part[0][27].rotasi=matriks_identitas();
  part[0][28].rotasi=matriks_identitas();
  part[0][29].rotasi=matriks_identitas();
  part[0][30].rotasi=matriks_identitas();
  
  part[1][0].rotasi=matriks_rotasi(0,0);
  part[1][1].rotasi=matriks_rotasi(2,0);
  part[1][2].rotasi=matriks_rotasi(1,0);
  part[1][3].rotasi=matriks_rotasi(0,0);
  part[1][4].rotasi=matriks_rotasi(0,0);
  part[1][5].rotasi=matriks_rotasi(2,0);
  part[1][6].rotasi=matriks_rotasi(2,0);
  part[1][7].rotasi=matriks_rotasi(1,0);
  part[1][8].rotasi=matriks_rotasi(1,0);
  part[1][9].rotasi=matriks_rotasi(0,0);
  part[1][10].rotasi=matriks_rotasi(0,0);
  part[1][11].rotasi=matriks_rotasi(2,0);
  part[1][12].rotasi=matriks_rotasi(2,0);
  part[1][13].rotasi=matriks_rotasi(1,0);
  part[1][14].rotasi=matriks_rotasi(1,0);
  part[1][15].rotasi=matriks_rotasi(1,0);
  part[1][16].rotasi=matriks_rotasi(0,0);
  part[1][17].rotasi=matriks_rotasi(0,0);
  part[1][18].rotasi=matriks_rotasi(2,0);
  part[1][19].rotasi=matriks_rotasi(2,-30);
  part[1][20].rotasi=matriks_rotasi(0,0);
  part[1][21].rotasi=matriks_rotasi(0,0);
  part[1][22].rotasi=matriks_rotasi(0,0);
  part[1][23].rotasi=matriks_rotasi(0,0);
  part[1][24].rotasi=matriks_rotasi(2,0);
  part[1][25].rotasi=matriks_rotasi(2,0);
  part[1][26].rotasi=matriks_rotasi(2,0);
  part[1][27].rotasi=matriks_identitas();
  part[1][28].rotasi=matriks_identitas();
  part[1][29].rotasi=matriks_identitas();
  part[1][30].rotasi=matriks_identitas();
  transformasi(part);
  
  
  
  //
  for(int i=0;i<27;i++){
      circle(width/4+part[0][i].koordinat_titik_berat_tertransformasi.elemen[0][0]*2/5,11*height/12-part[0][i].koordinat_titik_berat_tertransformasi.elemen[1][0]*2/5,8);
  }
  
  line(width/8,2*height/5,width/8+100,2*height/5);
  line(width/8+100,2*height/5,width/8+100,2*height/5-150);
  line(width/8+100,2*height/5-150,width/8,2*height/5-150);
  line(width/8,2*height/5-150,width/8,2*height/5);
  
  line(width/8+part[0][27].koordinat_titik_berat_tertransformasi.elemen[0][0],2*height/5-part[0][27].koordinat_titik_berat_tertransformasi.elemen[2][0],width/8+part[0][28].koordinat_titik_berat_tertransformasi.elemen[0][0],2*height/5-part[0][28].koordinat_titik_berat_tertransformasi.elemen[2][0]);
  line(width/8+part[0][28].koordinat_titik_berat_tertransformasi.elemen[0][0],2*height/5-part[0][28].koordinat_titik_berat_tertransformasi.elemen[2][0],width/8+part[0][29].koordinat_titik_berat_tertransformasi.elemen[0][0],2*height/5-part[0][29].koordinat_titik_berat_tertransformasi.elemen[2][0]);
  line(width/8+part[0][29].koordinat_titik_berat_tertransformasi.elemen[0][0],2*height/5-part[0][29].koordinat_titik_berat_tertransformasi.elemen[2][0],width/8+part[0][30].koordinat_titik_berat_tertransformasi.elemen[0][0],2*height/5-part[0][30].koordinat_titik_berat_tertransformasi.elemen[2][0]);
  line(width/8+part[0][30].koordinat_titik_berat_tertransformasi.elemen[0][0],2*height/5-part[0][30].koordinat_titik_berat_tertransformasi.elemen[2][0],width/8+part[0][27].koordinat_titik_berat_tertransformasi.elemen[0][0],2*height/5-part[0][27].koordinat_titik_berat_tertransformasi.elemen[2][0]);
  
  circle(width/8+titik_berat_x_L(),2*height/5-titik_berat_z_L(),30);
  
  for(int i=0;i<27;i++){
      circle(3*width/4+part[1][i].koordinat_titik_berat_tertransformasi.elemen[0][0]*2/5,11*height/12-part[1][i].koordinat_titik_berat_tertransformasi.elemen[1][0]*2/5,8);
  }
  
  line(6*width/8,2*height/5,6*width/8+100,2*height/5);
  line(6*width/8+100,2*height/5,6*width/8+100,2*height/5-150);
  line(6*width/8+100,2*height/5-150,6*width/8,2*height/5-150);
  line(6*width/8,2*height/5-150,6*width/8,2*height/5);
  
  //line();
  
  circle(6*width/8+titik_berat_x_R(),2*height/5-titik_berat_z_R(),30);
}
