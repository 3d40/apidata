from django import forms
from .models import *

class DataUtamaForm(forms.Form):
    nama = forms.CharField(label='Nama', max_length=100)
    nip = forms.CharField(label='NIP', max_length=100)
    jabatan = forms.CharField(label='Jabatan', max_length=100)
    pangkat = forms.CharField(label='Pangkat Golongan Ruang', max_length=100)
    opd = forms.CharField(label='Organisasi Perangkat Daerah', max_length=100)
    unitkerja = forms.CharField(label='Uni Kerja', max_length=100)

class CariForm(forms.Form):
    nip = forms.CharField(label='NIP', max_length=100)

class DataPangkatForm(forms.Form):
    jenis = forms.CharField(label='Jenis', max_length=100)
    golongan = forms.CharField(label='Pangkat Golongan Ruang', max_length=100)
    tmt = forms.CharField(label='Terhitung Mulai Tanggal', max_length=100)
    status = forms.CharField(label='Status Berkas', max_length=100)


class FormKarisKarsu(forms.Form):
    skpns = forms.BooleanField(label = 'Berkas PNS', disabled=True)
    skcpns = forms.BooleanField(label= 'Berkas CPNS', disabled=True)
    skakhir = forms.BooleanField(label= 'Berkas Pangkat Terakhir', disabled=True)

class FormIstri(forms.Form):
    status = forms.BooleanField(label = 'Akta Nikah', disabled=True)

class FormPengKarsu(forms.ModelForm):
    class Meta:
        model = ModelTLayananKarisKarsu
        fields =  ['jenis','orang', 'opd', 'pendukung', 'formulir']
