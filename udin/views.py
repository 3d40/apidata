from django.shortcuts import render
from apiload.models import ModelTRiwayatPangkat, ModelTDataUtama
from urllib.request import  urlopen
import json

from django.http import HttpRequest, HttpResponse


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

def IndexView(request):
    konsumen= request.user
    data = ModelTDataUtama.objects.get(nip=konsumen)
    listpkt = ModelTRiwayatPangkat.objects.filter(nama =data.pangkat).last()

    dbjabatan = urlopen(jabatan +str(konsumen))
    jsonjabatan = json.load(dbjabatan)


    return HttpResponse('OKE')



