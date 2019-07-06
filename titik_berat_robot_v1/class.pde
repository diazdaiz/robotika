class Matriks{
  int banyak_baris, banyak_kolom;
  float[][] elemen=new float[10][10];
}

class Part{
  Matriks koordinat_titik_berat_default=new Matriks();
  Matriks koordinat_sumbu_rotasi_servo=new Matriks();
  Matriks rotasi=new Matriks();
  Matriks koordinat_titik_berat_tertransformasi=new Matriks();
  int parent;
  float massa;
}
