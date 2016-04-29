from django.shortcuts import render, redirect

from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from quickstart.serializers import UserSerializer, GroupSerializer


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
from vigilantjourney.settings.production_heroku import CHANNEL_ID, CHANNEL_SECRET, CHANNEL_MID

def linebot(request):
    print('test')
    response = HttpResponse(content_type='application/json; charset=UTF-8')
    response['X-Line-ChannelID'] = CHANNEL_ID
    response['X-Line-ChannelSecret'] = CHANNEL_SECRET
    response['X-Line-Trusted-User-With-ACL'] = CHANNEL_MID

    return render(request, 'quickstart/base.html', {'response': response})
