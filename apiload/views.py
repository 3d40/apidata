from django.shortcuts import render, get_object_or_404, HttpResponse, redirect, get_list_or_404,reverse
from urllib.request import  urlopen, URLopener
from .forms import *
import json
from . signals import *


from django.http import HttpRequest, HttpResponse
from . import signals
import ssl

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
            'jabatan':json_pegawai[0]['field_jabatan_1'],
            'pangkat':json_pegawai[0]['field_pangkat'],
            'opd':json_pegawai[0]['field_perangkat_daerah'],
            'unitkerja':json_pegawai[0]['field_unit_kerja']
        }
        form = DataUtamaForm(initial=context)
        return render(request,'apiload/datautama.html', {'form':form})
    return render(request, 'apiload/cari.html',{'form':form})




def index(request: HttpRequest) -> HttpResponse:
    header = '''<!DOCTYPE html>
<html>
  <head>
    <title>BONCES API</title>
    <meta name="viewport" content="width=device-width, height=device-height, initial-scale=1.0, minimum-scale=1.0">
  </head>
  <body>
  <h1>TEST KONEKSI</h1>'''

    footer = '''<p>Prakom BKD</p>
    <ul>
        <li><a href="http://data.bkd.jambiprov.go.id">Hompe Page</a></li>
    </ul>
  </body>
</html>'''

    if request.user.is_authenticated:
        body = """
        <p>You logged in as <strong>%s</strong>.</p>
        <p><a href="/cari">cari</a></p>
        <p><a href="/accounts/logout">Logout</a></p>
         """ % request.user.username
    else:
        body = '<p><a href="/accounts/login">Login</a></p>'

    return HttpResponse(header + body + footer)

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

