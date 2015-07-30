# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from oauth2_provider.oauth2_backends import OAuthLibCore


class KeepRequestCore(OAuthLibCore):
    """
    Subclass of OAuthLibCore used only for the sake of keeping the django
    request object by placing it in the headers.
    This is a hack and we need a better solution for this.
    """
    def _extract_params(self, request):
        uri, http_method, body, headers = super(KeepRequestCore, self)._extract_params(request)
        headers["Django-request-object"] = request
        return uri, http_method, body, headers
