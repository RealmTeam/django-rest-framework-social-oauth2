from django.conf.urls import include
from oauth2_provider.views import AuthorizationView
from django.urls import re_path

from .views import ConvertTokenView, TokenView, RevokeTokenView, invalidate_sessions, DisconnectBackendView

app_name = 'drfso2'

urlpatterns = [
    re_path(r'^authorize/?$', AuthorizationView.as_view(), name="authorize"),
    re_path(r'^token/?$', TokenView.as_view(), name="token"),
    re_path('', include('social_django.urls', namespace="social")),
    re_path(r'^convert-token/?$', ConvertTokenView.as_view(), name="convert_token"),
    re_path(r'^revoke-token/?$', RevokeTokenView.as_view(), name="revoke_token"),
    re_path(r'^invalidate-sessions/?$', invalidate_sessions, name="invalidate_sessions"),
    re_path(r'^disconnect-backend/?$', DisconnectBackendView.as_view(), name="disconnect_backend")
]




