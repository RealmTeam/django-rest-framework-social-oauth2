import logging

from django.http import HttpRequest

from oauthlib.common import Request
from oauthlib.oauth2.rfc6749.endpoints.token import TokenEndpoint
from oauthlib.oauth2.rfc6749.tokens import BearerToken
from oauthlib.oauth2.rfc6749.endpoints.base import catch_errors_and_unavailability

from .oauth2_grants import SocialTokenGrant

log = logging.getLogger(__name__)


class SocialTokenServer(TokenEndpoint):
    """An endpoint used only for token generation.

    Use this with the KeepRequestCore backend class.
    """

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
        self._params = {}
        refresh_grant = SocialTokenGrant(request_validator)
        bearer = BearerToken(request_validator, token_generator,
                             token_expires_in, refresh_token_generator)
        TokenEndpoint.__init__(self, default_grant_type='convert_token',
                               grant_types={
                                   'convert_token': refresh_grant,
                               },
                               default_token_type=bearer)

    def set_request_object(self, request):
        """This should be called by the KeepRequestCore backend class before
        calling `create_token_response` to store the Django request object.
        """
        if not isinstance(request, HttpRequest):
            raise TypeError(
                "request must be an instance of 'django.http.HttpRequest'"
            )
        self._params['http_request'] = request

    def pop_request_object(self):
        """This is called internaly by `create_token_response`
        to fetch the Django request object and cleanup class instance.
        """
        return self._params.pop('http_request', None)

    # We override this method just so we can pass the django request object
    @catch_errors_and_unavailability
    def create_token_response(self, uri, http_method='GET', body=None,
                              headers=None, credentials=None):
        """Extract grant_type and route to the designated handler."""
        request = Request(
            uri, http_method=http_method, body=body, headers=headers)
        request.scopes = None
        request.extra_credentials = credentials

        # Make sure we consume the django request object
        request.django_request = self.pop_request_object()

        grant_type_handler = self.grant_types.get(request.grant_type,
                                                  self.default_grant_type_handler)
        log.debug('Dispatching grant_type %s request to %r.',
                  request.grant_type, grant_type_handler)
        return grant_type_handler.create_token_response(
            request, self.default_token_type)
