Change log
==========

1.2.0 - 2024-01-12
------------------

- Add support for Django 4.0
- Drop support for python 2, enforce python >=3.5
- Reference the User model with get_user_model()
- Fix ACCESS_TOKEN_URL namespace
- Refactor README
- Bump dependencies
- Remove django-braces dependency
- Set Django request object through a server method call
- Added a new Django Rest Framework view to disconnect backend
- Update documentation with Google example
- Create manage.py command to create an application
- Remove harcoded oauthlibcore
- Fix NoRerverseMatch Error with custom namespace
- Updated invalidate_sessions to accept all POST content types
- Restore compatibility with Django<2.0
- Keep request.data mutable
- Added compatibility with Django 2.0

1.1.0 - 2018-01-25
------------------

- <missing changelog>

1.0.8 - 2017-06-18
------------------

- Added `django-braces` as a dependency

1.0.7 - 2017-06-17
------------------

- Added support for `django-oauth-toolkit` 1.0.0

1.0.6 - 2017-05-22
------------------

- Fix a bug where inactive users could still get tokens


1.0.5 - 2017-01-03
------------------

- Updated python-social-auth to social (`Migrating guide <https://github.com/omab/python-social-auth/blob/master/MIGRATING_TO_SOCIAL.md>`_)
- Wrapped token view and revoke token view in a rest framework APIView
- Added url namespace
- Renamed PROPRIETARY_BACKEND_NAME to DRFSO2_PROPRIETARY_BACKEND_NAME


1.0.2 - 2015-08-11
------------------

- Fix a bug where the hack to keep the django request was not working due to oauthlib encoding the object

1.0.1 - 2015-08-09
------------------

- Forgot to update django-oauth-toolkit version in setup.py (version 0.9.0 needed because of `this change <https://github.com/evonove/django-oauth-toolkit/commit/6bdee6d3a8c481dffaa68038cf3418b4f83c8f10>`_)

1.0.0 - 2015-07-30
------------------

- Convert token view api changed and is now more conform to the oauth2 api.
- Removed PROPRIETARY_BACKEND_NAME setting
- Invalidate sessions view now takes a client_id as a parameter
