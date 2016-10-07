# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from social.backends.oauth import BaseOAuth2

from .settings import PROPRIETARY_BACKEND_NAME, REST_AUTH_URL_NAMESPACE


class DjangoOAuth2(BaseOAuth2):
    """Default OAuth2 authentication backend used by this package"""
    name = PROPRIETARY_BACKEND_NAME
    AUTHORIZATION_URL = reverse(REST_AUTH_URL_NAMESPACE + ':authorize')
    ACCESS_TOKEN_URL = reverse(REST_AUTH_URL_NAMESPACE + ':token')
