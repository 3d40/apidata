import datetime

from django.db import models
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw

class ModelTUser(models.Model):
    orang = models.CharField(max_length=100, db_column='nip')
    role =  models.CharField(max_length=100, null=True)
    class Meta:
        managed = False
        db_table = 't_user'
    def __str__(self):
        return str(self.orang)

# Create your models here.
class ModelTRiwayatPangkat(models.Model):
    id = models.BigAutoField(primary_key=True)
    orang = models.CharField(max_length=100 )
    nama = models.CharField(max_length=100, null=True, blank=True)
    jenis = models.CharField(max_length=100, null=True, blank=True)
    tmt = models.CharField(max_length=20, null=True, blank=True)
    status = models.CharField(max_length=100, null=True, blank=True)
    simbol = models.CharField(max_length=100, null=True, blank=True)
    mktahun = models.IntegerField(null=True, blank=True)
    mkbulan = models.IntegerField(null=True, blank=True)
    class Meta:
        managed = False
        db_table = 't_riwayat_pangkat'
    def __str__(self):
        return str(self.nama)

class ModelTPasangan(models.Model):
    id = models.BigAutoField(primary_key=True)
    nama = models.CharField(max_length=100 )
    orang = models.CharField(max_length=100 )
    akta = models.CharField(max_length=100, null=True, blank=True)
    tgl_nikah = models.CharField(max_length=100, null=True, blank=True)
    status_nikah = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=100, null=True, blank=True)
    class Meta:
        managed = False
        db_table = 't_pasangan'
    def __str__(self):
        return str(self.nama)

class ModelTOpd(models.Model):
    ids =models.IntegerField()
    nama = models.CharField(max_length=255)
    leader = models.CharField(max_length=255)
    class Meta:
        managed = False
        db_table = 't_opd'
    
    def __str__(self):
        return str(self.nama)


class ModelTDataUtama(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    nip = models.CharField(max_length=100, blank=True, null=True)
    jenis_asn = models.CharField(max_length=100, blank=True, null=True)
    nik = models.CharField(max_length=100, blank=True, null=True)
    pangkat = models.CharField(max_length=100, blank=True, null=True)
    golongan = models.CharField(max_length=100, blank=True, null=True)
    eselon = models.CharField(max_length=100, blank=True, null=True)
    jenis_jabatan = models.CharField(max_length=100, blank=True, null=True)
    jabatan = models.CharField(max_length=255, blank=True, null=True)
    instansi = models.CharField(max_length=100, blank=True, null=True)
    perangkat_daerah = models.CharField(max_length=255, blank=True, null=True)
    unit_kerja = models.CharField(max_length=255, blank=True, null=True)
    tempat_lahir = models.CharField(max_length=255, blank=True, null=True)
    tgl_lahir = models.CharField(max_length=255, blank=True, null=True)
    gol_darah = models.CharField(max_length=255, blank=True, null=True)
    telpon = models.CharField(max_length=255, blank=True, null=True)
    jenis_kelamin = models.CharField(max_length=255, blank=True, null=True)
    status_pernikahan = models.CharField(max_length=255, blank=True, null=True)
    agama = models.CharField(max_length=255, blank=True, null=True)
    alamat = models.CharField(max_length=255, blank=True, null=True)
    kecamatan = models.CharField(max_length=255, blank=True, null=True)
    kabupaten = models.CharField(max_length=255, blank=True, null=True)
    provinsi = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField()
    glr_belakang = models.CharField(max_length=255, blank=True, null=True)
    glr_depan = models.CharField(max_length=255, blank=True, null=True)
    tmt_cpns = models.CharField(max_length=255, blank=True, null=True)
    bup = models.IntegerField()
    kel_jab = models.IntegerField()
    
    class Meta:
        managed = False
        db_table = 't_data_utama'
    def __str__(self):
        return str(self.title)



class ModelTLayananKarisKarsu(models.Model):
    orang = models.CharField(max_length=100)
    opd = models.CharField(max_length=255)
    pendukung= models.ImageField(upload_to = "media")
    formulir = models.ImageField(upload_to = "media")
    jenis = models.ForeignKey('TJenisPengajuan',  on_delete=models.DO_NOTHING, blank=True, null=True)
    veropd = models.DateField()
    verbkd = models.DateField()
    verbkn = models.DateField()
    tolak = models.DateField()
    selesai = models.DateField()
    siapa = models.CharField(max_length=100)
    code = models.ImageField(blank=True, null=True, upload_to='code')

    class Meta:
        managed = False
        db_table = 't_layanan_karis_karsu'
    def __str__(self):
        return str(self.orang)
    
    def save(self, *arg, **kwargs):
        qr_image = qrcode.make(self.orang)
        qr_offset = Image.new('RGB', (310,310), white)
        qr_offset.paste(qr_image)
        files_name= f'{self.orang}-{self.id}.qr.png'
        stream = BytesIO()
        qr_offset.save(stream, 'PNG')
        self.code.save(files_name,File(stream), save=False)
        qr_offset.close()
        super().save(*arg, **kwargs)

class TJenisPengajuan(models.Model):
    nama = models.CharField(max_length=100)
    keterangan = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 't_jenis_pengajuan'
    def __str__(self):
        return str(self.nama)

