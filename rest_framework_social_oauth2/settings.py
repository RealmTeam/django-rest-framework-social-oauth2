# -*- coding: utf-8 -*-
from django.conf import settings

PROPRIETARY_BACKEND_NAME = getattr(settings, 'PROPRIETARY_BACKEND_NAME', "Django")
