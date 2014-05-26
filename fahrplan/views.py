from django.core.serializers.json import DjangoJSONEncoder
import json
from django.contrib.auth import authenticate, logout, login
from django.http import HttpResponse
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response
from fahrplan.models import *


@csrf_exempt
def index(request):
    if not request.user.is_authenticated():
        return render_to_response('login.html', {}, RequestContext(request))
    else:
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
            return answer({'success': True})
    else:
        return answer({'success': False})

@csrf_exempt
def user_logout(request):
    if request.user.is_authenticated():
        logout(request=request)

    return answer({'success': True})

@csrf_exempt
def autocomplete(request):
    userInput = request.POST.get('haltestelle', '')
    haltestellen = []

    for hs in Haltestelle.objects.all():
        if userInput.lower() in hs.name.lower():
            haltestellen.append(hs.name)

    return answer(haltestellen)

def answer(data):
    """Simplify response calls in JSON"""
    return HttpResponse(json.dumps(data, cls=DjangoJSONEncoder), content_type='application/json')