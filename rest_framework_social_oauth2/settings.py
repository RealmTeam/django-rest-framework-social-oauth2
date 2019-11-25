from django.conf import settings

DRFSO2_PROPRIETARY_BACKEND_NAME = getattr(settings, 'DRFSO2_PROPRIETARY_BACKEND_NAME', "Django")
DRFSO2_URL_NAMESPACE = getattr(settings, 'DRFSO2_URL_NAMESPACE', "")
