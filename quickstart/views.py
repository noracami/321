from django.shortcuts import get_object_or_404, render, redirect

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from quickstart.serializers import UserSerializer, GroupSerializer, FriendSerializer
from quickstart.models import Friend

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


class FriendViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows friends to be viewed or edited.
    """
    queryset = Friend.objects.all()
    serializer_class = FriendSerializer

from quickstart import LINE_HEADERS
LINE_ENDPOINT = 'https://trialbot-api.line.me'

def apptest(request, params=None):
    from .apps import QuickstartConfig
    data = QuickstartConfig.tMID
    return HttpResponse(data, status=200)

def isValidChannelSignature(key, content, signature):
    calc = base64.b64encode(hmac.new(key, content, digestmod=hashlib.sha256).digest())
    if calc != signature:
        print('received: %s' % signature)
        print('calculate: %s' % calc)
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

    #WSGIRequest append HTTP_ to headers
    if 'HTTP_X_LINE_CHANNELSIGNATURE' not in request.META:
        print('No X-LINE-ChannelSignature')
    else:
        print('There is a ChannelSignature: %s...' % request.META['HTTP_X_LINE_CHANNELSIGNATURE'][:8])
        if not isValidChannelSignature(
                LINE_HEADERS['X-Line-ChannelSecret'].encode('utf-8'), request.body,
                request.META['HTTP_X_LINE_CHANNELSIGNATURE'].encode('utf-8')):
            print('The request does not have a Valid Signature')

    req = json.loads(request.body.decode('utf-8'))

    if 'result' not in req:
        print('There is no result in request.json')
        return HttpResponse(status=470)
    #Receiving messages/operations
    else:
        line_friends_need_ask_name = []
        for data in req['result']:
            if 'content' not in data:
                print('There is no content in result')
                return HttpResponse(status=470)
            #Received operation
            if data['eventType'] == '138311609100106403':
                uid = data['content']['params'][0]
                #Added as friend or canceling block
                if data['content']['opType'] == 4:
                    if Friend.objects.filter(mid=uid):
                        yy = get_object_or_404(Friend, mid=uid)
                    else:
                        yy = Friend(mid=uid)
                        yy.save()
                    if not yy.was_edited_recently(days=1) or yy.name == 'username':
                        askName([uid])
                    text = '%s, Welcome to 9453!' % yy.name
                    sendTextMessage(uid, text, 'instruction')
                #Blocked account)
                elif data['content']['opType'] == 8:
                    print('user %s has block you.' % uid)
                    return HttpResponse(status=200)
            #Received message
            elif data['eventType'] == '138311609000106303':
                uid = data['content']['from']
                text = data['content']['text']
                if text is None:
                    print('text is None')
                    return HttpResponse(status=470)
                #TODO
                parseTextMessage(uid, text)
                #sendTextMessage(uid, text)
            else:
                print('unknown eventType!')
                return HttpResponse(status=470)
        return HttpResponse(status=200)

def askName(mids):
    payload = {
        'mids' : mids,
    }
    r = requests.get(LINE_ENDPOINT + '/v1/profiles', params=payload, headers=LINE_HEADERS)
    users = json.loads(r.text)['contacts']
    for user in users:
        name = user['displayName']
        friend = get_object_or_404(Friend, mid=user['mid'])
        friend.name = name
        friend.save()

def parseTextMessage(sender, text, case=None):

    if case == 'send_from_webconsole':
        return sendTextMessage(sender, text, case)
    elif 'book' in text:
        sendTextMessage(sender, text, 'book')
    else:
        sendTextMessage(sender, text, case)

def sendTextMessage(sender, text, case=None):
    if case is None:
        '''
        sendTextMessage
        '''
        text = 'Hello World.\n' + text
    elif case == 'instruction':
        '''
        send instruction for use
        '''
        text = "try 'book <something you like>'"
    elif case == 'send_from_webconsole':
        '''
        sendTextMessage
        '''
        text = 'Hello from another World.\n' + text
    elif case == 'book':
        '''
        prepare to  find the price of the book
        '''
        from quickstart.price import PriceInvestigator
        sendTextMessage(sender, "let's find the book")
        book = text.split('book')[1]
        print(book)
        a = PriceInvestigator()
        a.askTAAZE(book, number=1)
        text = a.price()
    else:
        return HttpResponse(status=470)
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
    pprint.pprint(json.dumps(data))

    r = requests.post(LINE_ENDPOINT + '/v1/events', data=json.dumps(data), headers=LINE_HEADERS)
    if r.status_code != requests.codes.ok:
        pprint.pprint(r.status_code)
        pprint.pprint(r.headers)
        pprint.pprint(r.text)
    if case == 'send_from_webconsole':
        return r
    else:
        print('complete')

@login_required(login_url='/api-auth/login/')
def webconsole(request):
    """
    for develop usage
    """

    """********"""
    """********"""

    property_list = {
        'M_DES_URL': '',
        'M_TEXT': '',
        'M_SENDER': '',
    }

    if request.method != 'POST':
        return render(request, 'quickstart/webconsole.html', {'response': 'NONE', 'property_list': property_list})

    for e in property_list:
        if e not in request.POST:
            property_list[e] = 'not exist'
        else:
            property_list[e] = request.POST[e]

    response = parseTextMessage(property_list['M_SENDER'], property_list['M_TEXT'], 'send_from_webconsole')
    return render(request, 'quickstart/webconsole.html', {'response': response, 'property_list': property_list})
