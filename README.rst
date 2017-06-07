Django rest-framework Social Oauth2
===================================

.. image:: https://badge.fury.io/py/django-rest-framework-social-oauth2.svg
    :target: http://badge.fury.io/py/django-rest-framework-social-oauth2

This module provides a python-social-auth and oauth2 support for django-rest-framework.

The first aim of this package is to help setting up social auth for your rest api. It also helps setting up your Oauth2 provider.

This package is relying on `python-social-auth <http://psa.matiasaguirre.net/docs/index.html>`_ and `django-oauth-toolkit <https://django-oauth-toolkit.readthedocs.org>`_.
You should probably read their docs if you were to go further than what is done here.
If you have some hard time understanding Oauth2 you can read a simple explanation `here <https://aaronparecki.com/articles/2012/07/29/1/oauth2-simplified>`_.


Installation
------------

Install with pip::

    pip install django-rest-framework-social-oauth2


Add these apps to your `INSTALLED_APPS`

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'oauth2_provider',
        'social_django',
        'rest_framework_social_oauth2',
    )


Include auth urls to your urls.py

.. code-block:: python

    urlpatterns = patterns(
        ...
        (r'^auth/', include('rest_framework_social_oauth2.urls')),
    )


Add these context processors to your `TEMPLATE_CONTEXT_PROCESSORS`

.. code-block:: python

    TEMPLATE_CONTEXT_PROCESSORS = (
        ...
        'social_django.context_processors.backends',
        'social_django.context_processors.login_redirect',
    )

Since Django version 1.8, the TEMPLATE_CONTEXT_PROCESSORS is deprecated, set the 'context_processors' option in the OPTIONS of a DjangoTemplates backend instead.

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

You can then enable the authentication classes for django rest framework by default or per view (add or update the `REST_FRAMEWORK` and `AUTHENTICATION_BACKENDS` entries to your settings.py)

.. code-block:: python

    REST_FRAMEWORK = {
        ...
        'DEFAULT_AUTHENTICATION_CLASSES': (
            ...
            'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
            'rest_framework_social_oauth2.authentication.SocialAuthentication',
        ),
    }

.. code-block:: python

    AUTHENTICATION_BACKENDS = (
        ...
       'rest_framework_social_oauth2.backends.DjangoOAuth2',
       'django.contrib.auth.backends.ModelBackend',
    )

The settings of this app are:
 - DRFSO2_PROPRIETARY_BACKEND_NAME sets the name of your Oauth2 social backend (e.g Facebook), defaults to "Django"
 - DRFSO2_URL_NAMESPACE sets the namespace for reversing urls.


Now go to django admin and add a new Application.
 - client_id and client_secret shouldn't be changed
 - user should be your superuser
 - redirect_uris should be left blank
 - client_type should be set to confidential
 - authorization_grant_type should be set to 'Resource owner password-based'
 - name can be set to whatever you want


The installation is done, you can now test the app.

Remember that you need to read the docs from `python-social-auth` and `django-oauth-toolkit` if you want to go further.
If you want to enable a social backend (like facebook), check the docs of `python-social-auth` about `supported backends <http://python-social-auth.readthedocs.io/en/latest/backends/index.html#supported-backends>`_ or `django-social-auth` about `bakends system <http://python-social-auth.readthedocs.io/en/latest/configuration/django.html>`_.


Testing the setup
-----------------

- Now that the installation is done, let's try it ! Ask a token for an user using curl :

    curl -X POST -d "client_id=<client_id>&client_secret=<client_secret>&grant_type=password&username=<user_name>&password=<password>" http://localhost:8000/auth/token

`<client_id>` and `<client_secret>` are the keys generated automatically that you can find in the model Application you created.

-  Now let's imagine you need to refresh your token :

    curl -X POST -d "grant_type=refresh_token&client_id=<client_id>&client_secret=<client_secret>&refresh_token=<your_refresh_token>" http://localhost:8000/auth/token

- Now let's try something else ! Let's exchange an external token for a token linked to your app :

    curl -X POST -d "grant_type=convert_token&client_id=<client_id>&client_secret=<client_secret>&backend=<backend>&token=<backend_token>" http://localhost:8000/auth/convert-token

`<backend>` here needs to be replaced by the name of an enabled backend (facebook for example if that's the case). Note that PROPRIETARY_BACKEND_NAME is a valid backend name but there is no use to do that here.
`<backend_token>` is for the token you got from the service utilizing an iOS app for example.

- Finally, let's try revoking tokens :

    - Revoke a single token :

        curl -X POST -d "client_id=<client_id>&client_secret=<client_secret>&token=<your_token>" http://localhost:8000/auth/revoke-token

    - Revoke all tokens for an user :

        curl -H "Authorization: Bearer <token>" -X POST -d "client_id=<client_id>" http://localhost:8000/auth/invalidate-sessions


If you have any questions feel free to ask me.


Social Authentication
---------------------

As you probably noticed, we enabled a default authentication backend called SocialAuthentication.
This backend lets you register and authenticate your users seamlessly on your api.

The class simply gets the backend name and token from the Authorization header and try to authenticate the user using the right external provider.

If the user was not registered on your app, it will create a new user to be used.

Example request :

    curl -H "Authorization: Bearer <backend_name> <backend_token>" http://localhost:8000/route/to/your/view


Facebook Example
----------------

To use Facebook as the authorization backend of your django-rest-framework api, your settings.py file should look like this:

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
            'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
            'rest_framework_social_oauth2.authentication.SocialAuthentication',
        )
    }

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

    # Define SOCIAL_AUTH_FACEBOOK_SCOPE to get extra permissions from facebook. Email is not sent by default, to get it, you must request the email permission:
    SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']
    SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
        'fields': 'id, name, email'
    }


- You can test these settings by running the following command :

    curl -X POST -d "grant_type=convert_token&client_id=<client_id>&client_secret=<client_secret>&backend=facebook&token=<facebook_token>" http://localhost:8000/auth/convert-token

This request returns the "access_token" that you should use on all HTTP requests with DRF. What is happening here is that we are converting a third-party access token (<user_access_token>) in an access token to use with your api and its clients ("access_token"). You should use this token on each and further communications between your system/application and your api to authenticate each request and avoid authenticating with FB every time.

You can find the id and secret of your app at https://developers.facebook.com/apps/.

For testing purposes you can use the access token `<user_access_token>` from https://developers.facebook.com/tools/accesstoken/.

For more information on how to configure python-social-auth with Facebook visit http://python-social-auth.readthedocs.io/en/latest/backends/facebook.html.
