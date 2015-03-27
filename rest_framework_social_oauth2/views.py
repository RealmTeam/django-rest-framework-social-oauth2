# -*- coding: utf-8 -*-

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions

from oauth2_provider.models import Application, AccessToken, RefreshToken
from oauthlib.common import generate_token

from .authentication import SocialAuthentication
from .settings import PROPRIETARY_APPLICATION_NAME

from datetime import datetime, timedelta

@api_view(['GET'])
@authentication_classes([SocialAuthentication])
@permission_classes([permissions.IsAuthenticated])
def convert_token(request):
    try:
        app = Application.objects.get(name=PROPRIETARY_APPLICATION_NAME)
    except Application.DoesNotExist:
        return Response({
            "detail": "The server's oauth2 application is not setup or misconfigured"
        }, status=status.HTTP_403_FORBIDDEN)

    code = status.HTTP_200_OK

    token = AccessToken.objects.filter(user=request.user, application=app).order_by('expires').last()
    if not token:
        token = AccessToken.objects.create(user=request.user, application=app,
            token=generate_token(), expires=datetime.now() + timedelta(days=1),
            scope="read write")
        refresh_token = RefreshToken.objects.create(access_token=token,
            token=generate_token(), user=request.user, application=app)
        code = status.HTTP_201_CREATED
    else:
        try:
            refresh_token = RefreshToken.objects.get(access_token=token,
                user=request.user, application=app)
        except RefreshToken.DoesNotExist:
            refresh_token = RefreshToken.objects.create(access_token=token,
                token=generate_token(), user=request.user, application=app)

    return Response({
        "access_token": token.token,
        "refresh_token": refresh_token.token,
        "token_type": "Bearer",
        "expires_in": int((token.expires - datetime.now()).total_seconds()),
        "scope": token.scope
    }, status=code)
