from django.db import models
from apiload.models import *

class ModelRiwayatJabatan(models.Model):
    field_nama_jabatan = models.CharField(max_length=255)
    field_jns_jabatan = models.CharField(max_length=255)
    field_tmt_jabatan = models.DateField()
    field_file_skk = models.CharField(max_length=255)
    moderation_state = models.CharField(max_length=255)
    
    class Meta:
        managed = False
        db_table = 'ModelRiwayatJabatan'
    def __str__(self):
        return str(self.field_nama_jabatan)

