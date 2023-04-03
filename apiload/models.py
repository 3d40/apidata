import datetime

from django.db import models
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw

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


# class ModelTAnak(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     orang = models.CharField(max_length=100 )
#     akta = models.CharField(max_length=100, null=True, blank=True)
#     status_nikah = models.CharField(max_length=100, null=True, blank=True)
#     status = models.CharField(max_length=100, null=True, blank=True)
#     class Meta:
#         managed = False
#         db_table = 't_anak'
#     def __str__(self):
#         return str(self.nama)

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

