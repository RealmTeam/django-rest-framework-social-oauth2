# -*- coding: utf-8 -*-
from django.conf import settings

PROPRIETARY_APPLICATION_NAME = getattr(settings, 'PROPRIETARY_APPLICATION_NAME', "Owner")
PROPRIETARY_BACKEND_NAME = getattr(settings, 'PROPRIETARY_BACKEND_NAME', "Django")
