# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from oauthlib.oauth2.rfc6749.endpoints.token import TokenEndpoint
from oauthlib.oauth2.rfc6749.tokens import BearerToken

from .oauth2_grants import SocialTokenGrant


class SocialTokenServer(TokenEndpoint):

    """An endpoint used only for token generation."""

    def __init__(self, request_validator, token_generator=None,
                 token_expires_in=None, refresh_token_generator=None, **kwargs):
        """Construct a client credentials grant server.
        :param request_validator: An implementation of
                                  oauthlib.oauth2.RequestValidator.
        :param token_expires_in: An int or a function to generate a token
                                 expiration offset (in seconds) given a
                                 oauthlib.common.Request object.
        :param token_generator: A function to generate a token from a request.
        :param refresh_token_generator: A function to generate a token from a
                                        request for the refresh token.
        :param kwargs: Extra parameters to pass to authorization-,
                       token-, resource-, and revocation-endpoint constructors.
        """
        refresh_grant = SocialTokenGrant(request_validator)
        bearer = BearerToken(request_validator, token_generator,
                             token_expires_in, refresh_token_generator)
        TokenEndpoint.__init__(self, default_grant_type='convert_token',
                               grant_types={
                                   'convert_token': refresh_grant,
                               },
                               default_token_type=bearer)
