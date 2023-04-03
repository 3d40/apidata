from django.urls import path
from .views import *


app_name = 'apiload'
urlpatterns = [
    path('', index, name='index'),
    path('pangkat', RiwayatPangkatView, name='rwpangkat'),
    path('jabatan', RiwayatJabatanView, name='rwjabatan'),
    path('pendidikan', RiwayatPendidikanView, name='rwpendidikan'),
    path('diklat', RiwayatDiklatView, name='rwdiklat'),
    path('pasangan', PasanganView, name='pasangan'),
    path('disiplin', RiwayatDisiplinView, name='disiplin'),
    path('cari', CariView, name='cari'),

    #Layanan
    path('kariskarsu', LayananKarisKarsu, name='karisu'),
    path('kariskarsu/formusalan', CetakFormView, name='formdownload'),
    path('kariskarsu/cekberkas', CekBerkasKarsuView, name='cekberkaskarsu'),
    path('kariskarsu/cekberkas/pengajuan', PengajuanKarisu, name='pengajuankarsu'),
    path('kariskarsu/cekberkas/ajukan', PengajuanKarisu, name='ajukankarsu'),

    path('opd', LoadOpd, name='opd'),
]

