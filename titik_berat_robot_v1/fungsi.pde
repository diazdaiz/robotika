//load data
void load(Part[][] part){
  Table table=loadTable("data.csv");
  TableRow row;
  for(int i=0;i<27;i++){
    row=table.getRow(i);
    part[0][i].koordinat_titik_berat_default.banyak_baris=3;
    part[0][i].koordinat_titik_berat_default.banyak_kolom=1;
    part[0][i].koordinat_titik_berat_default.elemen[0][0]=row.getFloat(0);
    part[0][i].koordinat_titik_berat_default.elemen[1][0]=row.getFloat(1);
    part[0][i].koordinat_titik_berat_default.elemen[2][0]=row.getFloat(2);
    part[0][i].koordinat_sumbu_rotasi_servo.banyak_baris=3;
    part[0][i].koordinat_sumbu_rotasi_servo.banyak_kolom=1;
    part[0][i].koordinat_sumbu_rotasi_servo.elemen[0][0]=row.getFloat(3);
    part[0][i].koordinat_sumbu_rotasi_servo.elemen[1][0]=row.getFloat(4);
    part[0][i].koordinat_sumbu_rotasi_servo.elemen[2][0]=row.getFloat(5);
    part[0][i].parent=row.getInt(6);
    part[0][i].massa=row.getFloat(7);
    part[1][i].koordinat_titik_berat_default.banyak_baris=3;
    part[1][i].koordinat_titik_berat_default.banyak_kolom=1;
    part[1][i].koordinat_titik_berat_default.elemen[0][0]=row.getFloat(8);
    part[1][i].koordinat_titik_berat_default.elemen[1][0]=row.getFloat(9);
    part[1][i].koordinat_titik_berat_default.elemen[2][0]=row.getFloat(10);
    part[1][i].koordinat_sumbu_rotasi_servo.banyak_baris=3;
    part[1][i].koordinat_sumbu_rotasi_servo.banyak_kolom=1;
    part[1][i].koordinat_sumbu_rotasi_servo.elemen[0][0]=row.getFloat(11);
    part[1][i].koordinat_sumbu_rotasi_servo.elemen[1][0]=row.getFloat(12);
    part[1][i].koordinat_sumbu_rotasi_servo.elemen[2][0]=row.getFloat(13);
    part[1][i].parent=row.getInt(14);
    part[1][i].massa=row.getFloat(15);
  }
}


//print matriks
void print_matriks(Matriks m1){
  for(int i=0; i<m1.banyak_baris; i++)
  {
    for(int j=0; j<m1.banyak_kolom; j++)
    {
      print(m1.elemen[i][j]," ");
    }
    println();
  }
}



//operasi matriks
void tambah(Matriks m1, Matriks m2, Matriks m3){
  float[][] mtemp;
  mtemp=new float[10][10];
  m3.banyak_baris=m1.banyak_baris;
  m3.banyak_kolom=m1.banyak_kolom;
  for(int i=0; i<m3.banyak_baris; i++)
  {
    for(int j=0; j<m3.banyak_kolom; j++)
    {
      mtemp[i][j]=m1.elemen[i][j]+m2.elemen[i][j];
    }
  }
  for(int i=0; i<=m3.banyak_baris; i++)
  {
    for(int j=0; j<=m3.banyak_kolom; j++)
    {
      m3.elemen[i][j]=mtemp[i][j];
    }
  }
}

void kurang(Matriks m1, Matriks m2, Matriks m3){
  float[][] mtemp;
  mtemp=new float[10][10];
  m3.banyak_baris=m1.banyak_baris;
  m3.banyak_kolom=m1.banyak_kolom;
  for(int i=0; i<m3.banyak_baris; i++)
  {
    for(int j=0; j<m3.banyak_kolom; j++)
    {
      mtemp[i][j]=m1.elemen[i][j]-m2.elemen[i][j];
    }
  }
  for(int i=0; i<=m3.banyak_baris; i++)
  {
    for(int j=0; j<=m3.banyak_kolom; j++)
    {
      m3.elemen[i][j]=mtemp[i][j];
    }
  }
}

void kali(Matriks m1, Matriks m2, Matriks m3){
  float[][] mtemp;
  mtemp=new float[10][10];
  float x;
  m3.banyak_baris=m1.banyak_baris;
  m3.banyak_kolom=m2.banyak_kolom;
  for(int i=0; i<m1.banyak_baris; i++)
  {
    for(int j=0; j<m2.banyak_kolom; j++)
    {  
      x=0;
      for(int k=0; k<m1.banyak_kolom; k++) //atau m2.banyak_baris juga bisa sebenernya
      {
        x=x+(m1.elemen[i][k]*m2.elemen[k][j]);
      }
      mtemp[i][j]=x;
    }
  }
  for(int i=0; i<m3.banyak_baris; i++)
  {
    for(int j=0; j<m3.banyak_kolom; j++)
    {
      m3.elemen[i][j]=mtemp[i][j];
    }
  }
}



//membuat matriks khusus
Matriks matriks_rotasi(int sumbu, float sudut){ //0x,1y,2z
  Matriks mtemp=new Matriks();
  int n;
  sudut=sudut*PI/180;
  mtemp.banyak_baris=3;
  mtemp.banyak_kolom=3;
  for(int i=0;i<3;i++){
    for(int j=0;j<3;j++){
      mtemp.elemen[i][j]=0;
    }
  }
  n=0;
  mtemp.elemen[sumbu][sumbu]=1;
  for(int i=0; i<2; i++){
    for(int j=0; j<2; j++){
      if(n==0){
        mtemp.elemen[(sumbu+i+1)%3][(sumbu+j+1)%3]=cos(sudut);
      }
      if(n==1){
        mtemp.elemen[(sumbu+i+1)%3][(sumbu+j+1)%3]=-sin(sudut);
      }
      if(n==2){
        mtemp.elemen[(sumbu+i+1)%3][(sumbu+j+1)%3]=sin(sudut);
      }
      if(n==3){
        mtemp.elemen[(sumbu+i+1)%3][(sumbu+j+1)%3]=cos(sudut);
      }
      n=n+1;
    }
  }
  return mtemp;
}

Matriks matriks_identitas(){
  Matriks mtemp=new Matriks();
  mtemp.banyak_baris=3;
  mtemp.banyak_kolom=3;
  for(int i=0; i<mtemp.banyak_baris; i++){
    for(int j=0; j<mtemp.banyak_kolom; j++){
      mtemp.elemen[i][j]=0;
    }
  }
  mtemp.elemen[0][0]=1;
  mtemp.elemen[1][1]=1;
  mtemp.elemen[2][2]=1;
  return mtemp;
}



//transformasi
void transformasi_0(Part part){
  kurang(part.koordinat_titik_berat_default, part.koordinat_sumbu_rotasi_servo, part.koordinat_titik_berat_tertransformasi);
  kali(part.rotasi, part.koordinat_titik_berat_tertransformasi, part.koordinat_titik_berat_tertransformasi);
  tambah(part.koordinat_titik_berat_tertransformasi, part.koordinat_sumbu_rotasi_servo, part.koordinat_titik_berat_tertransformasi);
}

void transformasi_1(Part[][] part, int kaki, int pe, int di){ //pentransformasi, ditransformasi
  kurang(part[kaki][di].koordinat_titik_berat_tertransformasi, part[kaki][pe].koordinat_sumbu_rotasi_servo, part[kaki][di].koordinat_titik_berat_tertransformasi);
  kali(part[kaki][pe].rotasi, part[kaki][di].koordinat_titik_berat_tertransformasi, part[kaki][di].koordinat_titik_berat_tertransformasi);
  tambah(part[kaki][di].koordinat_titik_berat_tertransformasi, part[kaki][pe].koordinat_sumbu_rotasi_servo, part[kaki][di].koordinat_titik_berat_tertransformasi);
  if(part[kaki][pe].parent!=-1){
    transformasi_1(part, kaki, part[kaki][pe].parent, di);
  }
}

void transformasi(Part[][] part){
  for(int i=0;i<27;i++){
    //kaki kiri
    transformasi_0(part[0][i]);
    if(part[0][i].parent!=-1){
      transformasi_1(part, 0, part[0][i].parent, i);
    }
    //kaki kanan
    transformasi_0(part[1][i]);
    if(part[1][i].parent!=-1){
      transformasi_1(part, 1, part[1][i].parent, i);
    }
  }
}
