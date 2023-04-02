import datetime

from django.shortcuts import render, get_object_or_404, HttpResponse, redirect, get_list_or_404,reverse
from urllib.request import  urlopen, URLopener
from .forms import *
import json
from . signals import *
from .models import *
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from dateutil.relativedelta import relativedelta
from django.http import HttpRequest, HttpResponse
from xhtml2pdf import pisa
from django.template.loader import get_template


datapokok = "http://data.bkd.jambiprov.go.id/rest-data-pokok/"#1X
displin = "http://data.bkd.jambiprov.go.id/rest-disiplin/"#2X
diklat = "http://data.bkd.jambiprov.go.id/rest-diklat/"#3X
jabatan = "http://data.bkd.jambiprov.go.id/rest-jabatan/"#4X
pangkat = "http://data.bkd.jambiprov.go.id/rest-pangkat/"#5X
anak = "http://data.bkd.jambiprov.go.id/rest-anak/"#6X
pasangan = "http://data.bkd.jambiprov.go.id/rest-suami-istri/"#7X
pendidikan = "http://data.bkd.jambiprov.go.id/rest-pendidikan/"#*X
opd = 'http://data.bkd.jambiprov.go.id/rest-kepala-opd'


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
            'unitkerja':json_pegawai[0]['field_unit_kerja'],

        }
        form = DataUtamaForm(initial=context)
    #     return render(request,'apiload/index.html', {'form':form})
    # return render(request, 'apiload/index.html  ',{'form':form})
        return render(request,'apiload/datautama.html', {'form':form})
    return render(request, 'apiload/cari.html', {'form':form})



def index(request: HttpRequest):
    if request.user.is_authenticated:
        nip = request.user
        data = urlopen(datapokok + str(nip))
        json_pegawai= json.load(data)
        pddkan = urlopen(pendidikan + str(nip))
        json_pddkan = json.load(pddkan)
        jumlahpddk = len(json_pddkan)-1

        pdkakhir = list(json_pddkan)
        tingakatpddkan = pdkakhir[jumlahpddk]
        w = tingakatpddkan['field_tingkat_pendidikan']
        print(w)
        pktakhir = ModelTRiwayatPangkat.objects.filter(orang= nip).latest('tmt')
        contex = {
            'user':request.user,
            'nama': json_pegawai[0]['field_nama'],
            'nip': nip,
            'jabatan': json_pegawai[0]['field_jabatan'],
            'pangkat': json_pegawai[0]['field_golongan'],
            'opd': json_pegawai[0]['field_perangkat_daerah'],
            'unitkerja': json_pegawai[0]['field_unit_kerja'],
            'user_picture':json_pegawai[0]['user_picture'],
            'golongan': json_pegawai[0]['field_golongan'],
            'telpon': json_pegawai[0]['field_handphone'],
            'alamat': json_pegawai[0]['field_alamat'],
            'jenisjabatan': json_pegawai[0]['field_jenis_jabatan'],
            'tgllahir': json_pegawai[0]['field_tanggal_lahir'],
            'tempatlahir': json_pegawai[0]['field_tempat_lahir'],
            'tingkat_pendidikan': w,
            'mktahun' : pktakhir.mktahun,
            'mkbulan': pktakhir.mkbulan,
        }
        return render(request, 'apiload/profile.html', contex)
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
    context = {
        'formpegawai': formpegawai,
        'formpasangan': formpasangan
    }
    nip = request.user
    data = urlopen(pangkat + str(nip))
    json_pegawai = json.load(data)
    datapasangan = urlopen(pasangan + str(nip))
    json_pasangan = json.load(datapasangan)
    for x in json_pegawai :
        ModelTRiwayatPangkat.objects.update_or_create(
                nama=x['field_pangkat'],
                orang=request.user,
                simbol=x['field_golongan'],
                tmt=x['field_tmt_golongan'],
                jenis=x['field_status_sk'],
                status=x['moderation_state']
            )
    for y in json_pasangan:
        ModelTPasangan.objects.update_or_create(
            nama=y['title'],
            orang=request.user,
            akta=y['field_nomor_akta_nikah'],
            status_nikah=y['field_status_pernikahan'],
            status=y['moderation_state'],
            tgl_nikah=y['field_tanggal_menikah']
            )
    lookpkt = ModelTRiwayatPangkat.objects.filter(orang = request.user)
    idpkakhir = lookpkt.latest('tmt')
    idpktawal = lookpkt.first()
    masakerja = relativedelta(datetime.strptime(idpkakhir.tmt,'%m-%d-%Y'), datetime.strptime(idpktawal.tmt,'%m-%d-%Y'))
    idpkakhir.mktahun = masakerja.years
    idpkakhir.mkbulan = masakerja.months
    idpkakhir.save()
    print(idpktawal.tmt, idpkakhir.tmt, masakerja.years, masakerja.months)
    if lookpkt.exists():
        try:
            idpkcpns = ModelTRiwayatPangkat.objects.get(jenis = "CPNS", orang = request.user)
            idpkpns = ModelTRiwayatPangkat.objects.get(jenis="PNS", simbol=idpkcpns.simbol, orang=request.user)
            # idpkakhir = lookpkt.last()
            # idpktawal = lookpkt.first()
            # print(idpktawal, idpkakhir)
            lookpasangan = ModelTPasangan.objects.get(orang=request.user)
            if idpkpns.status == "Valid" and idpkcpns.status == "Valid" and idpkakhir.status == "Valid" and lookpasangan.status =="Valid":
                formpegawai = FormKarisKarsu(initial={'skpns': True, 'skcpns': True, 'skakhir': True})
                formpasangan = FormIstri(initial={'status':True})
                context = {
                    'formpegawai':formpegawai,
                    'formpasangan':formpasangan
                }
            else:
                context = {
                    'formpegawai': formpegawai,
                    'formpasangan': formpasangan
                }
                return render(request, 'apiload/kariskarsu.html', context)
        except:
            pass
    return render(request, 'apiload/kariskarsu.html', context)


def LoadOpd(request):
    data = urlopen(opd)
    json_opd = json.load(data)
    for list_opd in json_opd:
        print(list_opd['name'])
        ModelTOpd.objects.update_or_create(
            ids = list_opd['field_perangkat_daerah_1'], 
            nama = list_opd['field_perangkat_daerah'], 
            leader = list_opd['name']
            )
    return HttpResponse("SUKSES")


def CetakFormView(request):
    nip = request.user
    datautama = urlopen(datapokok + str(nip))
    json_pegawai = json.load(datautama)
    pasangans = urlopen(pasangan + str(nip))
    json_pasangan = json.load(pasangans)
    anaks = urlopen(anak + str(nip))
    json_anak = json.load(anaks)

    template_path = 'apiload/kariskarsuform.html'
    context = {
        'anak':json_anak,
        'ístri': json_pasangan[0]['title'],
        'user': request.user,
        'nama': json_pegawai[0]['field_nama'],
        'nip': nip,
        'jabatan': json_pegawai[0]['field_jabatan'],
        'pangkat': json_pegawai[0]['field_golongan'],
        'opd': json_pegawai[0]['field_perangkat_daerah'],
        'unitkerja': json_pegawai[0]['field_unit_kerja'],
        'user_picture': json_pegawai[0]['user_picture'],
        'golongan': json_pegawai[0]['field_golongan'],
        'telpon': json_pegawai[0]['field_handphone'],
        'alamat': json_pegawai[0]['field_alamat'],
        'jenisjabatan': json_pegawai[0]['field_jenis_jabatan'],
        'tgllahir': json_pegawai[0]['field_tanggal_lahir'],
        'tempatlahir': json_pegawai[0]['field_tempat_lahir'],
        }
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="FormUsulanKarisKarsu.pdf"'
    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response



