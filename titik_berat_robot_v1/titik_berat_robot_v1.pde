Part[][] part=new Part[2][27]; //0=kaki kiri, 1=kaki kanan

void setup(){
  size(1000,600);
  background(75,120,75);
  for(int i=0; i<27; i++){
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
  part[0][19].rotasi=matriks_rotasi(2,0);
  part[0][20].rotasi=matriks_rotasi(0,0);
  part[0][21].rotasi=matriks_rotasi(0,0);
  part[0][22].rotasi=matriks_rotasi(0,0);
  part[0][23].rotasi=matriks_rotasi(0,0);
  part[0][24].rotasi=matriks_rotasi(2,0);
  part[0][25].rotasi=matriks_rotasi(2,0);
  part[0][26].rotasi=matriks_rotasi(2,30);
  
  //
  transformasi(part);
  for(int i=0;i<27;i++){
      circle(width/8+part[0][i].koordinat_titik_berat_tertransformasi.elemen[0][0]*2/5,11*height/12-part[0][i].koordinat_titik_berat_tertransformasi.elemen[1][0]*2/5,8);
  }
}
