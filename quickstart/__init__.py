import os

def _setting_module():
    return os.environ['DJANGO_SETTINGS_MODULE']

if _setting_module() == 'vigilantjourney.settings.local':
    CHANNEL_ID = '1234567890'
    CHANNEL_SECRET = 'secret'
    CHANNEL_MID = '0123456789'
elif _setting_module() == 'vigilantjourney.settings.production_heroku':
    CHANNEL_ID = os.environ['ChannelID']
    CHANNEL_SECRET = os.environ['ChannelSecret']
    CHANNEL_MID = os.environ['MID']
