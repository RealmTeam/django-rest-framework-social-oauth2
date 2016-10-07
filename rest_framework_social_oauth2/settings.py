# -*- coding: utf-8 -*-
from django.conf import settings

# TODO: this setting is deprecated, add a deprecation notice
PROPRIETARY_BACKEND_NAME = getattr(settings, 'PROPRIETARY_BACKEND_NAME', "Django")

REST_AUTH_BACKEND_NAME = getattr(settings, 'REST_AUTH_BACKEND_NAME', PROPRIETARY_BACKEND_NAME)
REST_AUTH_URL_NAMESPACE = getattr(settings, 'REST_AUTH_URL_NAMESPACE', 'rest_framework_social_oauth2')
