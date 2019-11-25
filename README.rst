Django REST Framework Social OAuth2
===================================

.. image:: https://badge.fury.io/py/django-rest-framework-social-oauth2.svg
    :target: http://badge.fury.io/py/django-rest-framework-social-oauth2

This module provides OAuth2 social authentication support for applications in Django REST Framework.

The aim of this package is to help set up social authentication for your REST API. It also helps setting up your OAuth2 provider.

This package relies on `python-social-auth <http://python-social-auth.readthedocs.io>`_ and `django-oauth-toolkit <https://django-oauth-toolkit.readthedocs.org>`_.
You should probably read their docs if you were to go further than what is done here.
If you have some hard time understanding OAuth2, you can read a simple explanation `here <https://aaronparecki.com/articles/2012/07/29/1/oauth2-simplified>`_.


Installation
------------

Install with pip::

    pip install django-rest-framework-social-oauth2


Add the following to your ``INSTALLED_APPS``:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'oauth2_provider',
        'social_django',
        'rest_framework_social_oauth2',
    )


Include social auth urls to your urls.py:

.. code-block:: python

    urlpatterns = patterns(
        ...
        (r'^auth/', include('rest_framework_social_oauth2.urls')),
    )


Add these context processors to your ``TEMPLATE_CONTEXT_PROCESSORS``:

.. code-block:: python

    TEMPLATE_CONTEXT_PROCESSORS = (
        ...
        'social_django.context_processors.backends',
        'social_django.context_processors.login_redirect',
    )

NB: since Django version 1.8, the ``TEMPLATE_CONTEXT_PROCESSORS`` is deprecated, set the ``'context_processors'`` option in the ``'OPTIONS'`` of a DjangoTemplates backend instead:

.. code-block:: python

    TEMPLATES = [
        {
            ...
            'OPTIONS': {
                'context_processors': [
                    ...
                    'social_django.context_processors.backends',
                    'social_django.context_processors.login_redirect',
                ],
            },
        }
    ]


You can then enable the authentication classes for Django REST Framework by default or per view (add or update the ``REST_FRAMEWORK`` and ``AUTHENTICATION_BACKENDS`` entries in your settings.py)

.. code-block:: python

    REST_FRAMEWORK = {
        ...
        'DEFAULT_AUTHENTICATION_CLASSES': (
            ...
            # 'oauth2_provider.ext.rest_framework.OAuth2Authentication',  # django-oauth-toolkit < 1.0.0
            'oauth2_provider.contrib.rest_framework.OAuth2Authentication',  # django-oauth-toolkit >= 1.0.0
            'rest_framework_social_oauth2.authentication.SocialAuthentication',
        ),
    }

.. code-block:: python

    AUTHENTICATION_BACKENDS = (
        ...
       'rest_framework_social_oauth2.backends.DjangoOAuth2',
       'django.contrib.auth.backends.ModelBackend',
    )


The settings of this  app are:

- ``DRFSO2_PROPRIETARY_BACKEND_NAME``: name of your OAuth2 social backend (e.g ``"Facebook"``), defaults to ``"Django"``
- ``DRFSO2_URL_NAMESPACE``: namespace for reversing URLs

Setting Up a New Application
----------------------------

Go to Django admin and add a new Application with the following configuration:

- ``client_id`` and ``client_secret`` should be left unchanged
- ``user`` should be your superuser
- ``redirect_uris`` should be left blank
- ``client_type`` should be set to ``confidential``
- ``authorization_grant_type`` should be set to ``'Resource owner password-based'``
- ``name`` can be set to whatever you'd like

The installation is done, you can now test the newly configured application.

It is recommended that you read the docs from `python-social-auth` and `django-oauth-toolkit` if you would like to go further. If you want to enable a social backend (e.g. Facebook), check the docs of `python-social-auth` on `supported backends <http://python-social-auth.readthedocs.io/en/latest/backends/index.html#supported-backends>`_ and `django-social-auth` on `backend configuration <http://python-social-auth.readthedocs.io/en/latest/configuration/django.html>`_.


Testing the Setup
-----------------

Now that the installation is done, let's try out the various functionality.
We will assume for the following examples that the REST API is reachable on ``http://localhost:8000``.

- Retrieve a token for a user using ``curl``::

    curl -X POST -d "client_id=<client_id>&client_secret=<client_secret>&grant_type=password&username=<user_name>&password=<password>" http://localhost:8000/auth/token

``<client_id>`` and ``<client_secret>`` are the keys generated automatically. you can find in the model Application you created.

-  Refresh token::

    curl -X POST -d "grant_type=refresh_token&client_id=<client_id>&client_secret=<client_secret>&refresh_token=<your_refresh_token>" http://localhost:8000/auth/token

- Exchange an external token for a token linked to your app::

    curl -X POST -d "grant_type=convert_token&client_id=<client_id>&client_secret=<client_secret>&backend=<backend>&token=<backend_token>" http://localhost:8000/auth/convert-token

``<backend>`` here needs to be replaced by the name of an enabled backend (e.g. "Facebook"). Note that ``PROPRIETARY_BACKEND_NAME`` is a valid backend name, but there is no use to do that here.
``<backend_token>`` is for the token you got from the service utilizing an iOS app for example.

- Revoke tokens:

    Revoke a single token::

        curl -X POST -d "client_id=<client_id>&client_secret=<client_secret>&token=<your_token>" http://localhost:8000/auth/revoke-token

    Revoke all tokens for a user::

        curl -H "Authorization: Bearer <token>" -X POST -d "client_id=<client_id>" http://localhost:8000/auth/invalidate-sessions


Authenticating Requests
-----------------------

As you have probably noticed, we enabled a default authentication backend called ``SocialAuthentication``.
This backend lets you register and authenticate your users seamlessly with your REST API.

The class simply retrieves the backend name and token from the Authorization header and tries to authenticate the user using the corresponding external provider. If the user was not yet registered on your app, it will automatically create a new user for this purpose.

Example authenticated request::

    curl -H "Authorization: Bearer <backend_name> <backend_token>" http://localhost:8000/route/to/your/view


Integration Examples
--------------------

For each authentication provider, the top portion of your REST API settings.py file should look like this:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        # OAuth
        'oauth2_provider',
        'social_django',
        'rest_framework_social_oauth2',
    )

    TEMPLATES = [
        {
            ...
            'OPTIONS': {
                'context_processors': [
                    ...
                    # OAuth
                    'social_django.context_processors.backends',
                    'social_django.context_processors.login_redirect',
                ],
            },
        }
    ]

    REST_FRAMEWORK = {
        ...
        'DEFAULT_AUTHENTICATION_CLASSES': (
            ...
            # OAuth
            # 'oauth2_provider.ext.rest_framework.OAuth2Authentication',  # django-oauth-toolkit < 1.0.0
            'oauth2_provider.contrib.rest_framework.OAuth2Authentication',  # django-oauth-toolkit >= 1.0.0
            'rest_framework_social_oauth2.authentication.SocialAuthentication',
        )
    }

Listed below are a few examples of supported backends that can be used for social authentication.


Facebook Example
^^^^^^^^^^^^^^^^

To use Facebook as the authorization backend of your REST API, your settings.py file should look like this:

.. code-block:: python

    AUTHENTICATION_BACKENDS = (
        # Others auth providers (e.g. Google, OpenId, etc)
        ...

        # Facebook OAuth2
        'social_core.backends.facebook.FacebookAppOAuth2',
        'social_core.backends.facebook.FacebookOAuth2',

        # django-rest-framework-social-oauth2
        'rest_framework_social_oauth2.backends.DjangoOAuth2',

        # Django
        'django.contrib.auth.backends.ModelBackend',
    )

    # Facebook configuration
    SOCIAL_AUTH_FACEBOOK_KEY = '<your app id goes here>'
    SOCIAL_AUTH_FACEBOOK_SECRET = '<your app secret goes here>'

    # Define SOCIAL_AUTH_FACEBOOK_SCOPE to get extra permissions from Facebook.
    # Email is not sent by default, to get it, you must request the email permission.
    SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']
    SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
        'fields': 'id, name, email'
    }

Remember to add this new Application in your Django admin (see section "Setting up Application").

You can test these settings by running the following command::

    curl -X POST -d "grant_type=convert_token&client_id=<client_id>&client_secret=<client_secret>&backend=facebook&token=<facebook_token>" http://localhost:8000/auth/convert-token

This request returns the "access_token" that you should use with every HTTP request to your REST API. What is happening here is that we are converting a third-party access token (``<user_access_token>``) to an access token to use with your API and its clients ("access_token"). You should use this token on each and further communications between your system/application and your api to authenticate each request and avoid authenticating with Facebook every time.

You can get the ID (``SOCIAL_AUTH_FACEBOOK_KEY``) and secret (``SOCIAL_AUTH_FACEBOOK_SECRET``) of your app at https://developers.facebook.com/apps/.

For testing purposes, you can use the access token ``<user_access_token>`` from https://developers.facebook.com/tools/accesstoken/.

For more information on how to configure python-social-auth with Facebook visit http://python-social-auth.readthedocs.io/en/latest/backends/facebook.html.


Google Example
^^^^^^^^^^^^^^

To use Google OAuth2 as the authorization backend of your REST API, your settings.py file should look like this:

.. code-block:: python

    AUTHENTICATION_BACKENDS = (
        # Others auth providers (e.g. Facebook, OpenId, etc)
        ...

	# Google OAuth2
	'social_core.backends.google.GoogleOAuth2',

        # django-rest-framework-social-oauth2
        'rest_framework_social_oauth2.backends.DjangoOAuth2',

        # Django
        'django.contrib.auth.backends.ModelBackend',
    )

    # Google configuration
    SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = <your app id goes here>
    SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = <your app secret goes here>

    # Define SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE to get extra permissions from Google.
    SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [
        'https://www.googleapis.com/auth/userinfo.email',
        'https://www.googleapis.com/auth/userinfo.profile',
    ]

Remember to add the new Application in your Django admin (see section "Setting up Application").

You can test these settings by running the following command::

    curl -X POST -d "grant_type=convert_token&client_id=<django-oauth-generated-client_id>&client_secret=<django-oauth-generated-client_secret>&backend=google-oauth2&token=<google_token>" http://localhost:8000/auth/convert-token

This request returns an "access_token" that you should use with every HTTP requests to your REST API. What is happening here is that we are converting a third-party access token (``<user_access_token>``) to an access token to use with your API and its clients ("access_token"). You should use this token on each and further communications between your system/application and your API to authenticate each request and avoid authenticating with Google every time.

You can get the ID (``SOCIAL_AUTH_GOOGLE_OAUTH2_KEY``) and secret (``SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET``) of your app at https://console.developers.google.com/apis/credentials
and more information on how to create one on https://developers.google.com/identity/protocols/OAuth2.

For testing purposes, you can use the access token ``<user_access_token>`` from https://developers.google.com/oauthplayground/.

For more information on how to configure python-social-auth with Google visit https://python-social-auth.readthedocs.io/en/latest/backends/google.html#google-oauth2.
