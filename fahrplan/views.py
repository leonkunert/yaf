from datetime import datetime
from django.core.serializers.json import DjangoJSONEncoder
import json
from django.contrib.auth import authenticate, logout, login
from django.http import HttpResponse
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response
import math
from fahrplan.models import *


@csrf_exempt
def fahrplan(request):
    return render_to_response('index.html', {}, RequestContext(request))

@csrf_exempt
def user_login(request):
    username = request.GET.get('user', '')
    password = request.GET.get('pass', '')
    user = authenticate(username=username, password=password)

    if user is not None:
        if user.is_active:
            login(request, user)
            return JSON_answer(True)
    else:
        return JSON_answer(False)

@csrf_exempt
def user_logout(request):
    if request.user.is_authenticated():
        logout(request=request)

    return JSON_answer(True)

@csrf_exempt
def user_status(request):
    userObj = {}
    if request.user.is_authenticated():
        userObj['username'] = request.user.username
        userObj['first_name'] = request.user.first_name
        userObj['last_name'] = request.user.last_name
        return JSON_answer(userObj)
    else:
        return JSON_answer(False)

@csrf_exempt
def getHaltestellen(request):
    haltestellen = []

    for hs in Haltestelle.objects.all():
        haltestellen.append(hs.name)

    haltestellen.sort()
    return JSON_answer(haltestellen)



def JSON_answer(data):
    """Simplify response calls in JSON"""
    return HttpResponse(json.dumps(data, cls=DjangoJSONEncoder), content_type='application/json')


@csrf_exempt
def getFahrtzeiten(request):
    haltestelle_string = request.GET.get('haltestelle', 'Bahnhof')
    #haltestelle_string = 'Berliner Platz'

    haltestelle = Haltestelle.objects.get(name=haltestelle_string)

    haltestellelinien = HaltestelleLinie.objects.filter(haltestelle=haltestelle)

    hsl = []
    for haltestellelinie in haltestellelinien:
        lin = {}
        lin['linie'] = haltestellelinie.linie.name
        lin['haltestellen'] = []

        linie = haltestellelinie.linie
        haltestellen = []
        for haltestellelinien in HaltestelleLinie.objects.filter(linie=linie).order_by('fahrtzeit'):
            haltestellen.append(haltestellelinien)
        for hs in haltestellen:
            hs.fahrtzeit -= haltestellelinie.fahrtzeit
            if hs.fahrtzeit >= 0:
                lin['haltestellen'].append({'name': hs.haltestelle.name, 'fahrtzeit': hs.fahrtzeit})
        hsl.append(lin)

    return JSON_answer(hsl)


@csrf_exempt
def getAbfahrtzeiten(request):
    #HALTESTELLE = "Berliner Platz"
    HALTESTELLE = request.GET.get('haltestelle', 'Bahnhof')
    weekday = datetime.weekday(datetime.now())

    haltestelle = Haltestelle.objects.get(name=HALTESTELLE)

    haltestellelinien = HaltestelleLinie.objects.filter(haltestelle=haltestelle)

    hsl = []
    for haltestellelinie in haltestellelinien:
        lin = {}
        lin['linie'] = haltestellelinie.linie.name

        linie = haltestellelinie.linie
        zeiten = []
        einsatzzeitenlinien = []
        for ezl in EinsatzzeitLinie.objects.filter(linie=linie):
            einsatzzeitenlinien.append(ezl)
        if weekday != '':
            for ezl in einsatzzeitenlinien:
                if ezl.einsatzzeit.bis_wochentag < weekday or weekday < ezl.einsatzzeit.von_wochentag:
                    einsatzzeitenlinien.remove(ezl)

        for ezl in einsatzzeitenlinien:
            uhrzeiten = []
            zeit = ezl.einsatzzeit.von_uhrzeit * 60
            pisszeit = ezl.einsatzzeit.bis_uhrzeit * 60
            while zeit <= pisszeit:
                uhrzeiten.append(zahl_zu_uhrzeit(zeit))
                zeit += ezl.einsatzzeit.takt
            lin['zeiten'] = uhrzeiten

        hsl.append(lin)

    #print json.dumps(hsl)
    return JSON_answer(hsl)


def zahl_zu_uhrzeit(z):
    hour = int(math.floor(z / 60))
    minute = z % 60

    if minute < 10:
        minute = '0{0}'.format(minute)

    return '{0}:{1}'.format(hour, minute)