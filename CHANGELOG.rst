Change log
==========

1.0.1 - 2015-08-09
-----------------

- Forgot to update django-oauth-toolkit version in setup.py (version 0.9.0 needed because of `this change <https://github.com/evonove/django-oauth-toolkit/commit/6bdee6d3a8c481dffaa68038cf3418b4f83c8f10>`_)

1.0.0 - 2015-07-30
-----------------

- Convert token view api changed and is now more conform to the oauth2 api.
- Removed PROPRIETARY_BACKEND_NAME setting
- Invalidate sessions view now takes a client_id as a parameter
