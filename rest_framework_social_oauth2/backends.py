# -*- coding: utf-8 -*-

from social_core.backends.oauth import BaseOAuth2
from django.core.urlresolvers import reverse
from .settings import DRFSO2_PROPRIETARY_BACKEND_NAME, DRFSO2_URL_NAMESPACE

class DjangoOAuth2(BaseOAuth2):
    """Default OAuth2 authentication backend used by this package"""
    name = DRFSO2_PROPRIETARY_BACKEND_NAME
    AUTHORIZATION_URL = reverse(DRFSO2_URL_NAMESPACE + ':authorize'
                                if DRFSO2_URL_NAMESPACE else 'authorize')
    ACCESS_TOKEN_URL = reverse(DRFSO2_URL_NAMESPACE + ':token'
                               if DRFSO2_URL_NAMESPACE else 'authorize')
