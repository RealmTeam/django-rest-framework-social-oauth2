# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse

from rest_framework.authentication import BaseAuthentication, get_authorization_header
from rest_framework import exceptions, HTTP_HEADER_ENCODING

from social.apps.django_app.views import NAMESPACE
from social.apps.django_app.utils import load_backend, load_strategy
from social.exceptions import MissingBackend
from social.utils import requests


class SocialAuthentication(BaseAuthentication):
    """
    Authentication backend using `python-social-auth`

    Clients should authenticate by passing the token key in the "Authorization"
    HTTP header with the backend used, prepended with the string "Bearer ".

    For example:

        Authorization: Bearer facebook 401f7ac837da42b97f613d789819ff93537bee6a
    """
    www_authenticate_realm = 'api'

    def authenticate(self, request):
        """
        Returns two-tuple of (user, token) if authentication succeeds,
        or None otherwise.
        """
        auth_header = get_authorization_header(request).decode(HTTP_HEADER_ENCODING)
        auth = auth_header.split()

        if not auth or auth[0].lower() != 'bearer':
            return None

        if len(auth) == 1:
            msg = 'Invalid token header. No backend provided.'
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) == 2:
            msg = 'Invalid token header. No credentials provided.'
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 3:
            msg = 'Invalid token header. Token string should not contain spaces.'
            raise exceptions.AuthenticationFailed(msg)

        token = auth[2]
        backend = auth[1]

        strategy = load_strategy(request=request)

        try:
            backend = load_backend(strategy, backend, reverse(NAMESPACE + ":complete", args=(backend,)))
        except MissingBackend:
            msg = 'Invalid token header. Invalid backend.'
            raise exceptions.AuthenticationFailed(msg)

        try:
            user = backend.do_auth(access_token=token)
        except requests.HTTPError as e:
            msg = e.response.text
            raise exceptions.AuthenticationFailed(msg)

        if not user:
            msg = 'Bad credentials.'
            raise exceptions.AuthenticationFailed(msg)
        return user, token

    def authenticate_header(self, request):
        """
        Bearer is the only finalized type currently
        """
        return 'Bearer backend realm="%s"' % self.www_authenticate_realm
