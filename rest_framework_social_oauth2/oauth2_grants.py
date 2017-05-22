# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import logging

from django.core.urlresolvers import reverse

from oauthlib.oauth2.rfc6749 import errors
from oauthlib.oauth2.rfc6749.grant_types.refresh_token import RefreshTokenGrant

from social_django.views import NAMESPACE
from social_django.utils import load_backend, load_strategy
from social_core.exceptions import MissingBackend, SocialAuthBaseException
from social_core.utils import requests


log = logging.getLogger(__name__)


class SocialTokenGrant(RefreshTokenGrant):

    """`Refresh token grant`_
    .. _`Refresh token grant`: http://tools.ietf.org/html/rfc6749#section-6
    """

    def validate_token_request(self, request):
        # This method's code is based on the parent method's code
        # We removed the original comments to replace with ours
        # explaining our modifications.

        # We need to set these at None by default otherwise
        # we are going to get some AttributeError later
        request._params.setdefault("backend", None)
        request._params.setdefault("client_secret", None)

        if request.grant_type != 'convert_token':
            raise errors.UnsupportedGrantTypeError(request=request)

        # We check that a token parameter is present.
        # It should contain the social token to be used with the backend
        if request.token is None:
            raise errors.InvalidRequestError(
                description='Missing token parameter.',
                request=request)

        # We check that a backend parameter is present.
        # It should contain the name of the social backend to be used
        if request.backend is None:
            raise errors.InvalidRequestError(
                description='Missing backend parameter.',
                request=request)

        if not request.client_id:
            raise errors.MissingClientIdError(request=request)

        if not self.request_validator.validate_client_id(request.client_id, request):
            raise errors.InvalidClientIdError(request=request)

        # Existing code to retrieve the application instance from the client id
        if self.request_validator.client_authentication_required(request):
            log.debug('Authenticating client, %r.', request)
            if not self.request_validator.authenticate_client(request):
                log.debug('Invalid client (%r), denying access.', request)
                raise errors.InvalidClientError(request=request)
        elif not self.request_validator.authenticate_client_id(request.client_id, request):
            log.debug('Client authentication failed, %r.', request)
            raise errors.InvalidClientError(request=request)

        # Ensure client is authorized use of this grant type
        # We chose refresh_token as a grant_type
        # as we don't want to modify all the codebase.
        # It is also the most permissive and logical grant for our needs.
        request.grant_type = "refresh_token"
        self.validate_grant_type(request)

        self.validate_scopes(request)

        # TODO: Find a better way to pass the django request object
        strategy = load_strategy(request=request.django_request)

        try:
            backend = load_backend(strategy, request.backend,
                                   reverse(NAMESPACE + ":complete", args=(request.backend,)))
        except MissingBackend:
            raise errors.InvalidRequestError(
                description='Invalid backend parameter.',
                request=request)

        try:
            user = backend.do_auth(access_token=request.token)
        except requests.HTTPError as e:
            raise errors.InvalidRequestError(
                description="Backend responded with HTTP{0}: {1}.".format(e.response.status_code,
                                                                          e.response.text),
                request=request)
        except SocialAuthBaseException as e:
            raise errors.AccessDeniedError(description=str(e), request=request)

        if not user:
            raise errors.InvalidGrantError('Invalid credentials given.', request=request)

        if not user.is_active:
            raise errors.InvalidGrantError('User inactive or deleted.', request=request)
        
        request.user = user
        log.debug('Authorizing access to user %r.', request.user)
