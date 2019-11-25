from oauth2_provider.oauth2_backends import OAuthLibCore
from oauth2_provider.settings import oauth2_settings

from .oauth2_endpoints import SocialTokenServer


class KeepRequestCore(oauth2_settings.OAUTH2_BACKEND_CLASS):
    """
    Subclass of `oauth2_settings.OAUTH2_BACKEND_CLASS`, used for the sake of
    keeping the Django request object by passing it through to the
    `server_class` instance.

    This backend should only be used in views with SocialTokenServer
    as the `server_class`.
    """

    def __init__(self, *args, **kwargs):
        super(KeepRequestCore, self).__init__(*args, **kwargs)
        if not isinstance(self.server, SocialTokenServer):
            raise TypeError(
                "server_class must be an instance of 'SocialTokenServer'"
            )

    def create_token_response(self, request):
        """
        A wrapper method that calls create_token_response on `server_class` instance.
        This method is modified to also pass the `django.http.HttpRequest`
        request object.

        :param request: The current django.http.HttpRequest object
        """
        self.server.set_request_object(request)
        return super(KeepRequestCore, self).create_token_response(request)
