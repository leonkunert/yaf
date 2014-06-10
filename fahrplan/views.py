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


@csrf_exempt
def getFahrtzeiten(request):
    haltestelle_string = request.GET.get('haltestelle', 'Bahnhof')

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
def getAbfahrtszeiten(request):
    haltestelle_string = request.GET.get('haltestelle', 'Bahnhof')
    weekday = datetime.weekday(datetime.now())

    haltestelle = Haltestelle.objects.get(name=haltestelle_string)

    haltestellelinien = HaltestelleLinie.objects.filter(haltestelle=haltestelle)

    hsl = []
    for haltestellelinie in haltestellelinien:
        lin = {}
        lin['linie'] = haltestellelinie.linie.name

        linie = haltestellelinie.linie
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

    return JSON_answer(hsl)


@csrf_exempt
def getDienstplan(request):
    user = request.user
    wochentage= [
        'Montag',
        'Dienstag',
        'Mittwoch',
        'Donnerstag',
        'Freitag',
        'Samstag',
        'Sonntag'
    ]

    if user is not None:
        print FahrerUserMap
        busfahrer = FahrerUserMap.objects.get(user=user).fahrer

        personalKurs = []
        for kurs in Kurs.objects.filter(fahrer=busfahrer).order_by('wochentag'):
            for ezl in EinsatzzeitLinie.objects.filter(linie=kurs.linie):
                ez = ezl.einsatzzeit
                if ez.von_wochentag <= kurs.wochentag <= ez.bis_wochentag:
                    tageskurs = {
                        'wochentag': wochentage[kurs.wochentag],
                        'schicht': kurs.schicht,
                        #'dienstbeginn': ez.von_uhrzeit + (8 * (kurs.schicht - 1)) + ((ez.takt/60) * (kurs.tour - 1)),
                        #'dienstschluss': ez.von_uhrzeit + (8 * kurs.schicht) + ((ez.takt/60) * kurs.tour - 1),
                        'bus': kurs.bus.nummer,
                        'linie': kurs.linie.name
                    }
                    ez.von_uhrzeit *= 60
                    ez.bis_uhrzeit *= 60
                    arbeitszeit = (ez.bis_uhrzeit - ez.von_uhrzeit)
                    if kurs.tour == 1:
                        delay = 0
                    else:
                        delay = ez.takt

                    if kurs.schicht == 1:
                        dienstbeginn = ez.von_uhrzeit + delay
                        dienstschluss = arbeitszeit / 2 + delay
                    else:
                        dienstbeginn = arbeitszeit / 2 + ez.von_uhrzeit + delay
                        dienstschluss = ez.bis_uhrzeit
                    tageskurs['dienstbeginn'] = zahl_zu_uhrzeit(dienstbeginn)
                    tageskurs['dienstschluss'] = zahl_zu_uhrzeit(dienstschluss)
                    personalKurs.append(tageskurs)

        #print json.dumps(personalKurs)
        return JSON_answer(personalKurs)
    else:
        return JSON_answer({'error': 'Busfahrer nicht gefunden. :('})



## HELPER FUNCTIONS ##

def zahl_zu_uhrzeit(z):
    hour = int(math.floor(z / 60))
    minute = int(math.floor(z % 60))

    if minute < 10:
        minute = '0{0}'.format(minute)

    return '{0}:{1}'.format(hour, minute)


def create_fahrer_accounts():
    for fahrer in Busfahrer.objects.all():
        fahrerUser = User.objects.create_user(
            username=fahrer.name.lower(),
            password='yaf',
            email='{0}@yaf.com'.format(fahrer.name.lower())
        )
        fahrerUser.first_name = fahrer.vorname
        fahrerUser.last_name = fahrer.name
        fahrerUser.save()

        fu = FahrerUserMap(fahrer=fahrer, user=fahrerUser)
        fu.save()


def JSON_answer(data):
    """Simplify response calls in JSON"""
    return HttpResponse(json.dumps(data, cls=DjangoJSONEncoder), content_type='application/json')