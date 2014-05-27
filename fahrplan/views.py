from django.core.serializers.json import DjangoJSONEncoder
import json
from django.contrib.auth import authenticate, logout, login
from django.http import HttpResponse
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response
from fahrplan.models import *


@csrf_exempt
def fahrplan(request):
    return render_to_response('index.html', {}, RequestContext(request))

@csrf_exempt
def user_login(request):
    username = request.GET.get('user', '')
    password = request.GET.get('pass', '')
    user = authenticate(username=username, password=password)
    print request

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


def test():
    # FAKE DATEN
    HALTESTELLE = "Berliner Platz"
    STARTHOUR = 12
    STARTMINUTE = 37

    haltestelle = Haltestelle.objects.get(name=HALTESTELLE)

    haltestellelinien = HaltestelleLinie.objects.filter(haltestelle=haltestelle)
    for hsl in haltestellelinien:
        fahrtHour = STARTHOUR
        fahrtMin = STARTMINUTE

        linie = hsl.linie
        initFahrtzeit = hsl.fahrtzeit
        print "[[ {0} ]]".format(linie.name)
        for hs in HaltestelleLinie.objects.filter(linie=linie):
            fahrtMin += hs.fahrtzeit - initFahrtzeit
            if fahrtMin >= 60:
                fahrtMin -= 60
                fahrtHour += 1
            if hs.haltestellennummer >= hsl.haltestellennummer:
                print " - " + hs.haltestelle.name + " (" + str(fahrtHour) + ":" + str(fahrtMin) +")"