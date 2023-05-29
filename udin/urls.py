from django.urls import path
from .views import *


app_name = 'udin'
urlpatterns = [

    #Layanan
    path('udin', IndexView, name='index'),
    # path('udin/formusalan', CetakFormView, name='formdownload'),
    # path('udin/cekberkas', CekBerkasKarsuView, name='cekberkaskarsu'),
    # path('udin/cekberkas/pengajuan', PengajuanKarisu, name='pengajuankarsu'),
    # path('udin/cekberkas/ajukan', PengajuanKarisu, name='ajukankarsu'),

    # path('opd', LoadOpd, name='opd'),
    # path('userall', userall, name='userall'),
    # path('datautama', IsiDataUatam, name='datautama'),

    # #OPD
    # path('listpegawai', PegawaiListView.as_view(), name='listpegawai'),


]
