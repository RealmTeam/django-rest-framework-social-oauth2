# -*- coding: utf-8 -*-

from django.conf.urls import url, include
from oauth2_provider.views import AuthorizationView, TokenView, RevokeTokenView

from .views import ConvertTokenView, invalidate_sessions

urlpatterns = [
    url(r'^authorize/?$', AuthorizationView.as_view(), name="authorize"),
    url(r'^token/?$', TokenView.as_view(), name="token"),
    url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'^convert-token/?$', ConvertTokenView.as_view(), name="convert_token"),
    url(r'^revoke-token/?$', RevokeTokenView.as_view(), name="revoke_token"),
    url(r'^invalidate-sessions/?$', invalidate_sessions, name="invalidate_sessions")
]
