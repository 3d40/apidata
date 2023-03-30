import datetime

from django.shortcuts import render, get_object_or_404, HttpResponse, redirect, get_list_or_404,reverse
from urllib.request import  urlopen, URLopener
from .forms import *
import json
from . signals import *
from .models import *
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist


from django.http import HttpRequest, HttpResponse

datapokok = "http://data.bkd.jambiprov.go.id/rest-data-pokok/"#1X
displin = "http://data.bkd.jambiprov.go.id/rest-disiplin/"#2X
diklat = "http://data.bkd.jambiprov.go.id/rest-diklat/"#3X
jabatan = "http://data.bkd.jambiprov.go.id/rest-jabatan/"#4X
pangkat = "http://data.bkd.jambiprov.go.id/rest-pangkat/"#5X
anak = "http://data.bkd.jambiprov.go.id/rest-anak/"#6X
pasangan = "http://data.bkd.jambiprov.go.id/rest-suami-istri/"#7X
pendidikan = "http://data.bkd.jambiprov.go.id/rest-pendidikan/"#*X


def CariView(request):
    """ search function  """
    form = CariForm
    if request.method == "POST":
        print(request)
        nip = request.POST.get('nip')
        data = urlopen(datapokok + str(nip))
        json_pegawai = json.load(data)
        request.session['nip'] = nip
        print(request.session['nip'])
        context = {
            'nama': json_pegawai[0]['field_nama'],
            'nip':nip,
            'jabatan':json_pegawai[0]['field_jabatan'],
            'pangkat':json_pegawai[0]['field_golongan'],
            'opd':json_pegawai[0]['field_perangkat_daerah'],
            'unitkerja':json_pegawai[0]['field_unit_kerja']
        }
        form = DataUtamaForm(initial=context)
    #     return render(request,'apiload/index.html', {'form':form})
    # return render(request, 'apiload/index.html  ',{'form':form})
        return render(request,'apiload/datautama.html', {'form':form})
    return render(request, 'apiload/cari.html', {'form':form})





def index(request: HttpRequest):
    if request.user.is_authenticated:
        context = {
            'user' : request.user,
        }
        return render(request, 'apiload/index.html', context)
    else:
        return redirect('cas_ng_login')

def ping(request: HttpRequest) -> HttpResponse:
    return HttpResponse('pong', content_type="text/plain")

def RiwayatPangkatView(request):
    nip = request.session['nip']
    data = urlopen(pangkat + str(nip))
    json_pegawai = json.load(data)
    context = {
        'data':json_pegawai
        }
    print(context)
    return render(request,'apiload/riwayatpangkat.html', context)


def RiwayatJabatanView(request):
    nip = request.session['nip']
    data = urlopen(jabatan + str(nip))
    json_pegawai = json.load(data)
    context = {
        'data':json_pegawai
        }
    print(context)
    return render(request,'apiload/riwayatjabatan.html', context)

def RiwayatPendidikanView(request):
    nip = request.session['nip']
    data = urlopen(pendidikan + str(nip))
    json_pegawai = json.load(data)
    context = {
        'data':json_pegawai
        }
    print(context)
    return render(request,'apiload/riwayatpendidikan.html', context)

def RiwayatDiklatView(request):
    nip = request.session['nip']
    data = urlopen(diklat + str(nip))
    json_pegawai = json.load(data)
    context = {
        'data':json_pegawai
        }
    print(context)
    return render(request,'apiload/riwayatdiklat.html', context)

def PasanganView(request):
    nip = request.session['nip']
    istri = urlopen(pasangan + str(nip))
    json_pasangan = json.load(istri)
    anaks = urlopen(anak + str(nip))
    json_anak = json.load(anaks)
    context = {
        'pasangan':json_pasangan,
        'anak':json_anak
        }
    print(context)
    return render(request,'apiload/keluarga.html', context)

def RiwayatDisiplinView(request):
    nip = request.session['nip']
    data = urlopen(displin + str(nip))
    json_pegawai = json.load(data)
    context = {
        'data':json_pegawai
        }
    print(context)
    return render(request,'apiload/riwayatdisiplin.html', context)


def LayananKarisKarsu(request):
    formpegawai = FormKarisKarsu
    formpasangan = FormIstri
    nip = request.user
    data = urlopen(pangkat + str(nip))
    json_pegawai = json.load(data)
    datapasangan = urlopen(pasangan + str(nip))
    json_pasangan = json.load(datapasangan)
    for x in json_pegawai :
        ModelTRiwayatPangkat.objects.update_or_create(
            nama = x['field_pangkat'],
            orang = request.user,
            simbol = x['field_golongan'],# tmt = datetime.strptime(x['field_tmt_golongan'], '%d-%m-%Y').date(),
            tmt=x['field_tmt_golongan'], 
            jenis = x['field_status_sk'], 
            status = x['moderation_state'] 
            )
    for y in json_pasangan :
        ModelTPasangan.objects.update_or_create(
            nama = y['title'], 
            orang = request.user, 
            akta = y['field_nomor_akta_nikah'], 
            status_nikah = y['field_status_pernikahan'], 
            status = y['moderation_state'],
            tgl_nikah = y['field_tanggal_menikah']
            )
    
    lookpkt = ModelTRiwayatPangkat.objects.filter(orang = request.user)
    lookpasangan = ModelTPasangan.objects.filter(orang = request.user)

    for pkt in lookpkt:
        try:
            idpkcpns = ModelTRiwayatPangkat.objects.get(jenis = "CPNS", orang = request.user)
        except ObjectDoesNotExist:
            return HttpResponse("Berkas Tidak Lengkap")

        try:
            idpkpns = ModelTRiwayatPangkat.objects.get(jenis = "PNS", simbol = x['field_golongan'], orang = request.user)
        except ObjectDoesNotExist:
            return HttpResponse("Berkas Tidak Lengkap")
        
        try:
            idpkakhir = lookpkt.last()
        except ObjectDoesNotExist:
            return HttpResponse("Berkas Tidak Lengkap")
        if idpkpns.status == "Valid" and idpkcpns.status == "Valid" and idpkakhir.status == "Valid":
            formpegawai = FormKarisKarsu(initial={'skpns':True, 'skcpns':True, 'skakhir':True})
        else:
            return HttpResponse("Berkas Tidak Lengkap")
        
        for bojo in lookpasangan:
            getpasangan = lookpasangan.get( orang = request.user)
            if getpasangan.status == "Valid" :
                formpasangan = FormIstri(initial={'status':True})
            else: 
                return HttpResponse("Berkas Tidak Lengkap")

        context= {
                'formpegawai':formpegawai,
                'formpasangan':formpasangan, 
            }
    return render(request,'apiload/kariskarsu.html', context)

