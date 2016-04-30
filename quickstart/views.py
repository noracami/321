from django.shortcuts import render, redirect

from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from quickstart.serializers import UserSerializer, GroupSerializer

import json
import pprint
import requests

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

LINE_ENDPOINT = 'https://trialbot-api.line.me'

LINE_HEADERS = {
    "Content-Type": 'application/json; charset=UTF-8',
    "X-Line-ChannelID": CHANNEL_ID,
    "X-Line-ChannelSecret": CHANNEL_SECRET,
    "X-Line-Trusted-User-With-ACL": CHANNEL_MID,
}

def linebot(request):

    """
    Receiving messages/operations

        Request specifications

        HTTPS is used to access the BOT API server from the LINE
        platform. The specifications for access requests are as follows.

            Protocol: HTTPS
            HTTP method: POST
            Content type: application/json; charset=UTF-8
            Target URL: URL registered on the Channel Console

        Example:

            POST /callback HTTP/1.1
            HOST: YOUR_SERVER_HOST_NAME
            Content-type: application/json; charset=UTF-8
            X-LINE-ChannelSignature: /abcd1234+Ab/U=

            {"result":[{...}, {...}]}

    Sending messages
    """

    import urllib

    print(request)

    pprint.pprint(request.body)
    req = json.loads(request.body.decode('utf-8'))

    pprint.pprint(request.POST)
    #pprint.pprint(request.META)
    pprint.pprint(req)

    print('-*-*-*-*-')

    if 'result' not in req:
        print('There is no result in request.json')
    else:
        result = req['result']
        for data in result:
            if 'content' in data:
                pprint.pprint('content: %s' % data['content'])
            pprint.pprint(data)

    sendTextMessage(data['content']['from'], data['content']['text'])


    #response = HttpResponse(content_type='application/json; charset=UTF-8')
    #response['X-Line-ChannelID'] = CHANNEL_ID
    #response['X-Line-ChannelSecret'] = CHANNEL_SECRET
    #response['X-Line-Trusted-User-With-ACL'] = CHANNEL_MID

    #print(request.body)

    #req = json.loads(request.body.decode('utf-8'))
    #pprint.pprint(req)

    #result = json.loads(request.readall().decode('utf-8'))

    #req['result'][0]['tesst'] = 'test'
    #received_json_data=json.loads(request.body)

    #if 'result' not in request.json:
    #    print('There is no result in request.json')
    #    return HttpResponse(status=470)
    #for req in request.json['result']:
    #    print(req)

    #print(received_json_data)

    #return JsonResponse(data=req)

    """
    send messages to users from your BOT API server.

    ---

    Endpoint host: trialbot-api.line.me
    Protocol: HTTPS
    Required request header:{
        X-Line-ChannelID: Channel ID
        X-Line-ChannelSecret: Channel secret
        X-Line-Trusted-User-With-ACL: MID (of Channel)
    }


    """

    print('complete')
    return HttpResponse(status=200)
    #return render(request, 'quickstart/base.html', {})

def sendTextMessage(sender, text):
    '''
    sendTextMessage
    '''
    text = 'Hello World.\n' + text
    data = {
        'to': [sender],
        'toChannel': 1383378250, #Fixed value
        'eventType': '138311608800106203', #Fixed value
        'content': {
            'contentType': 1, #Fixed value
            'toType': 1, #To user
            'text': text
        }
    }
    print('send: ' % data)

    r = requests.post(LINE_ENDPOINT + '/v1/events', data=json.dumps(data), headers=LINE_HEADERS)
    if r.status_code != requests.codes.ok:
        pprint.pprint(r.status_code)
        pprint.pprint(r.headers)
        pprint.pprint(r.body)
