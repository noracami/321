import os

def _setting_module():
    return os.environ['DJANGO_SETTINGS_MODULE']

if _setting_module() == 'vigilantjourney.settings.local':
    __CHANNEL_ID__ = '1234567890'
    __CHANNEL_SECRET__ = 'secret'
    __CHANNEL_MID__ = '0123456789'
elif _setting_module() == 'vigilantjourney.settings.production_heroku':
    __CHANNEL_ID__ = os.environ['ChannelID']
    __CHANNEL_SECRET__ = os.environ['ChannelSecret']
    __CHANNEL_MID__ = os.environ['MID']

LINE_HEADERS = {
    "Content-Type": 'application/json; charset=UTF-8',
    "X-Line-ChannelID": __CHANNEL_ID__,
    "X-Line-ChannelSecret": __CHANNEL_SECRET__,
    "X-Line-Trusted-User-With-ACL": __CHANNEL_MID__,
}
