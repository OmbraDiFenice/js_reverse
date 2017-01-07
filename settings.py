from django.conf import settings as user_settings
from .apps import JsReverseConfig as App

settings = getattr(user_settings, App.name.upper(), {})

ALL_NAMES = settings.get('ALL_NAMES', '*')
JS_OBJECT_NAME = settings.get('JS_OBJECT_NAME', 'Url')