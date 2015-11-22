# -*- coding: utf-8 -*-

from django.http import HttpResponse
from braces.views import CsrfExemptMixin

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import permissions

from oauth2_provider.models import Application, AccessToken
from oauth2_provider.settings import oauth2_settings
from oauth2_provider.views.mixins import OAuthLibMixin
from oauth2_provider.ext.rest_framework import OAuth2Authentication

from .oauth2_backends import KeepRequestCore
from .oauth2_endpoints import SocialTokenServer


class ConvertTokenView(CsrfExemptMixin, OAuthLibMixin, APIView):
    """
    Implements an endpoint to provide access tokens
    The endpoint is used in the following flows:
    * Authorization code
    * Password
    * Client credentials
    """
    permission_classes = (AllowAny,)
    server_class = SocialTokenServer
    validator_class = oauth2_settings.OAUTH2_VALIDATOR_CLASS
    oauthlib_backend_class = KeepRequestCore

    def post(self, request, *args, **kwargs):
        url, headers, body, status = self.create_token_response(request)
        response = HttpResponse(content=body, status=status)

        for k, v in headers.items():
            response[k] = v
        return response


@api_view(['POST'])
@authentication_classes([OAuth2Authentication])
@permission_classes([permissions.IsAuthenticated])
def invalidate_sessions(request):
    client_id = request.POST.get("client_id", None)
    if client_id is None:
        return Response({
            "client_id": ["This field is required."]
        }, status=status.HTTP_400_BAD_REQUEST)

    try:
        app = Application.objects.get(client_id=client_id)
    except Application.DoesNotExist:
        return Response({
            "detail": "The application linked to the provided client_id could not be found."
        }, status=status.HTTP_400_BAD_REQUEST)

    tokens = AccessToken.objects.filter(user=request.user, application=app)
    tokens.delete()
    return Response({}, status=status.HTTP_204_NO_CONTENT)
