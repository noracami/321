from django.shortcuts import render, redirect

from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from quickstart.serializers import UserSerializer, GroupSerializer

import json

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


from django.http import HttpResponse
from django.http.response import JsonResponse

import os

if os.environ['DJANGO_SETTINGS_MODULE'] == 'vigilantjourney.settings.local':
    from vigilantjourney.settings.local import CHANNEL_ID, CHANNEL_SECRET, CHANNEL_MID
elif os.environ['DJANGO_SETTINGS_MODULE'] == 'vigilantjourney.settings.production_heroku':
    from vigilantjourney.settings.production_heroku import CHANNEL_ID, CHANNEL_SECRET, CHANNEL_MID

def linebot(request):
    print('test')
    response = HttpResponse(content_type='application/json; charset=UTF-8')
    response['X-Line-ChannelID'] = CHANNEL_ID
    response['X-Line-ChannelSecret'] = CHANNEL_SECRET
    response['X-Line-Trusted-User-With-ACL'] = CHANNEL_MID

    #print(request.body)

    req = json.loads(request.body.decode('utf-8'))

    #result = json.loads(request.readall().decode('utf-8'))

    import pprint

    pprint.pprint(req)

    #req['result'][0]['tesst'] = 'test'
    #received_json_data=json.loads(request.body)

    #if 'result' not in request.json:
    #    print('There is no result in request.json')
    #    return HttpResponse(status=470)
    #for req in request.json['result']:
    #    print(req)

    #print(received_json_data)

    print('success')
    #return JsonResponse(data=req)
    return HttpResponse(status=200)
    #return render(request, 'quickstart/base.html', {})
