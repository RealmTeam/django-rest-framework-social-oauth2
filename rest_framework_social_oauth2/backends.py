# -*- coding: utf-8 -*-

from social.backends.oauth import BaseOAuth2
from django.core.urlresolvers import reverse
from .settings import PROPRIETARY_BACKEND_NAME

class DjangoOAuth2(BaseOAuth2):
    """Default OAuth2 authentication backend used by this package"""
    name = PROPRIETARY_BACKEND_NAME
    AUTHORIZATION_URL = reverse('authorize')
    ACCESS_TOKEN_URL = reverse('token')