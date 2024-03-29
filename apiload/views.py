import datetime

from django.shortcuts import render, get_object_or_404, HttpResponse, redirect, get_list_or_404,reverse
from urllib.request import  urlopen, URLopener
from .forms import *
import json
from . signals import *
from .models import *
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from dateutil.relativedelta import  relativedelta
from django.http import HttpRequest, HttpResponse
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.contrib import messages
from django.views.generic.list import ListView


datapokok = "http://data.bkd.jambiprov.go.id/rest-data-pokok/"#1X
displin = "http://data.bkd.jambiprov.go.id/rest-disiplin/"#2X
diklat = "http://data.bkd.jambiprov.go.id/rest-diklat/"#3X
jabatan = "http://data.bkd.jambiprov.go.id/rest-jabatan/"#4X
pangkat = "http://data.bkd.jambiprov.go.id/rest-pangkat/"#5X
anak = "http://data.bkd.jambiprov.go.id/rest-anak/"#6X
pasangan = "http://data.bkd.jambiprov.go.id/rest-suami-istri/"#7X
pendidikan = "http://data.bkd.jambiprov.go.id/rest-pendidikan/"#*X
opd = 'http://data.bkd.jambiprov.go.id/rest-kepala-opd'
userlayanan = '/home/bonces/baru/apidata/apiload/rest-user-all.json'


def userall(request):
    data = open(userlayanan)
    pengguna = json.load(data)
    for gust in pengguna:
        ModelTUser.objects.update_or_create(
            orang = gust['name'],
            role = gust['roles_target_id']
        )
    return HttpResponse("SUKSES")


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

def addpkt (request):
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
    if request.user.is_authenticated:
        return redirect('apiload:index')
    else:
        return redirect('cas_ng_login')


def index(request):
    nip = request.user
    lookpkt = ModelTRiwayatPangkat.objects.filter(orang=nip).order_by('tmt')
    idpktawal = lookpkt.first()
    print(idpktawal)
    idpkakhir = lookpkt.last()
    masakerja = relativedelta(datetime.strptime(idpkakhir.tmt,'%m-%d-%Y'), datetime.strptime(idpktawal.tmt,'%m-%d-%Y'))
    idpkakhir.mktahun = masakerja.years
    idpkakhir.mkbulan = masakerja.months
    idpkakhir.save()

    if request.user.is_authenticated:
        cekuser = get_object_or_404(ModelTUser, orang = request.user)
        if cekuser.role == "":
            cekuser.role = "Pegawai"
            print(cekuser.role) 
            nip = request.user
            data = urlopen(datapokok + str(nip))
            json_pegawai= json.load(data)
            pddkan = urlopen(pendidikan + str(nip))
            tgllhrstr = json_pegawai[0]['field_tanggal_lahir']
            tmtbup = json_pegawai[0]['field_bup']
            tgllhr = datetime.strptime(tgllhrstr,'%d-%m-%Y')
            tmtpensiun = datetime.date(tgllhr + relativedelta(years=int(tmtbup)))
            json_pddkan = json.load(pddkan)
            jumlahpddk = len(json_pddkan)-1
            pdkakhir = list(json_pddkan)
            tingakatpddkan = pdkakhir[jumlahpddk]
            w = tingakatpddkan['field_tingkat_pendidikan']

            context={
                'bup' : tmtbup,
                'pensiun': tmtpensiun,
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
                'mktahun' : idpkakhir.mktahun,
                'mkbulan': idpkakhir.mkbulan,
            }
            return render(request, 'apiload/profile.html', context)
        elif cekuser.role == "OPD":
            return render(request, )

    else:
        return redirect('cas_ng_login')

def ping(request: HttpRequest) -> HttpResponse:
    return HttpResponse('pong', content_type="text/plain")

def RiwayatPangkatView(request):
    nip = request.user
    data = urlopen(pangkat + str(nip))
    json_pegawai = json.load(data)
    print(json_pegawai)  
    context = {
        'data':json_pegawai
        }
    print(context)
    return render(request,'apiload/rwgolongan_list.html', context)


def RiwayatJabatanView(request):
    nip = request.user
    data = urlopen(jabatan + str(nip))
    json_pegawai = json.load(data)
    context = {
        'data':json_pegawai
        }
    print(context)
    return render(request,'apiload/riwayatjabatan.html', context)

def RiwayatPendidikanView(request):
    nip = request.user
    data = urlopen(pendidikan + str(nip))
    json_pegawai = json.load(data)
    context = {
        'data':json_pegawai
        }
    print(context)
    return render(request,'apiload/riwayatpendidikan.html', context)

def RiwayatDiklatView(request):
    nip = request.user
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
    nip = request.user
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

    return render(request, 'apiload/kariskarsu.html', context)

def PengajuanKarisKarsu(request):
    form = FormKarisKarsu
    context= {
        'form':form
    }
    return render(request, 'apiload/pengajuankariskarsu.html', context)


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


def CekBerkasKarsuView(request):
    nip = request.user
    formpegawai = FormKarisKarsu()
    formpasangan = FormIstri()
    context = {
            'formpegawai': formpegawai,
            'formpasangan': formpasangan
        }

    data = urlopen(pangkat + str(nip))
    json_pegawai = json.load(data)
    jmlhpkt = len(json_pegawai)-1
    bojo = urlopen(pasangan + str(nip))
    json_bojo = json.load(bojo)
    bojos = json_bojo[0]['moderation_state']
    cpns = json_pegawai[0]['moderation_state']
    pns = json_pegawai[1]['moderation_state']
    akhir = json_pegawai[jmlhpkt]['moderation_state']
    if cpns == "Valid" and pns == "Valid" and akhir == "Valid" and bojos == "Valid":
        formpegawai = FormKarisKarsu(initial ={'skcpns':True, 'skpns':True, 'skakhir':True})
        formpasangan = FormIstri(initial ={'status':True})
        context = {
            'formpegawai': formpegawai,
            'formpasangan': formpasangan
        }
        return render(request, 'apiload/kariskarsufix.html', context)
    else:
        messages.warning(request, "Data belum lengkap!!!")
        return render(request, 'apiload/kariskarsufix.html', context)


# def PengajuanKarisu(request):
#     nip = request.user
#     data = urlopen(datapokok + str(nip))
#     json_pegawai = json.load(data)
#     form = FormPengKarsu(initial ={
#         'orang':json_pegawai[0]['field_nama'],
#         'opd': json_pegawai[0]['field_perangkat_daerah'],
#     })
#     if request.method =='POST':
#         form = form(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return HttpResponse("SUKSES")
#     else:
#         return render(request, 'apiload/formpengkarsu.html',{'form':form} )

def PengajuanKarisu(request):
    nip = request.user
    data = urlopen(datapokok + str(nip))
    json_pegawai = json.load(data)
    form = FormPengKarsu()
    print(form)
    if request.method=='POST':
        form = FormPengKarsu(request.POST, instance={
            'orang':json_pegawai[0]['field_nama'],
            'opd': json_pegawai[0]['field_perangkat_daerah'],
            })
        if form.is_valid():
            form.save()
            return render(request, 'apiload/kariskarsufix.html', {'form':form})
    return redirect('apiload:index')


def IsiDataUatam(requset):
    pengguna = ModelTUser.objects.all()
    for data in pengguna:
        pokok = urlopen(datapokok + str(data.orang))
        json_pegawai = json.load(pokok)
        print(json_pegawai)
    return HttpResponse("Banyak Nian")


class PegawaiListView(ListView):
    template_name = 'opd/modeltdatautama_list.html'
    
    def get(self, request):
        nip = self.request.user
        cekuser = ModelTUser.objects.get(orang=self.request.user)
        jenis = cekuser.role
        if jenis == "":
            # return redirect ('apiload:index')
            pegawai = ModelTDataUtama.objects.filter(perangkat_daerah = 'Badan Kepegawaian Daerah')
            context = {'object_list': pegawai}
            return render(request,'opd/modeltdatautama_list.html',context)
        elif  jenis == "OPD":
            pegawai = ModelTDataUtama.objects.filter(perangkat_daerah = 'Badan Kepegawaian Daerah')
            context = {'object_list': pegawai}
            return render(request,'opd/modeltdatautama_list.html',context)
    