from django.shortcuts import render, redirect

from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from quickstart.serializers import UserSerializer, GroupSerializer


from django.http import HttpResponse

import base64
import hashlib
import hmac
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


from quickstart import LINE_HEADERS
LINE_ENDPOINT = 'https://trialbot-api.line.me'

def apptest(request, params=None):
    from .apps import QuickstartConfig
    data = QuickstartConfig.tMID
    return HttpResponse(data, status=200)

def isValidChannelSignature(key, content, signature):
    print(signature)
    calc = base64.b64encode(hmac.new(secret_key, request.body, digestmod=hashlib.sha256).digest())
    print(calc)
    if calc != request.META['X-LINE-ChannelSignature']:
        return False
    else:
        return True

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

    pprint.pprint(request.META)
    return HttpResponse(status=200)

    if 'X-LINE-ChannelSignature' '''not''' in request.META:
        print('There is a X-LINE-ChannelSignature')

    if not isValidChannelSignature(
            LINE_HEADERS['X-Line-ChannelSecret'], request.body,
            request.META['X-LINE-ChannelSignature']):
        print('The request does not have a Valid Signature')

    req = json.loads(request.body.decode('utf-8'))

    if 'result' not in req:
        print('There is no result in request.json')
        return HttpResponse(status=470)
    #Receiving messages/operations
    else:
        for data in req['result']:
            if 'content' not in data:
                print('There is no content in result')
                return HttpResponse(status=470)
            #Received operation
            if data['eventType'] == '138311609100106403':
                uid = data['content']['params'][0]
                text = 'Hello'
            #Received message
            elif data['eventType'] == '138311609100106303':
                uid = data['content']['from']
                text = data['content']['text']
                if text is None:
                    print('text is None')
                    return HttpResponse(status=470)
            sendTextMessage(uid, text)
    print('complete')
    return HttpResponse(status=200)

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
            'contentType': 1, #Text message, Fixed value
            'toType': 1, #To user
            'text': text
        }
    }
    print('send:')
    pprint.pprint(json.loads(data))

    r = requests.post(LINE_ENDPOINT + '/v1/events', data=json.dumps(data), headers=LINE_HEADERS)
    if r.status_code != requests.codes.ok:
        pprint.pprint(r.status_code)
        pprint.pprint(r.headers)
        pprint.pprint(r.text)
