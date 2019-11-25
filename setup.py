from setuptools import setup, find_packages
import sys

if sys.version_info < (3, 5):
    raise SystemError("This package is for Python 3.5 and above.")

setup(
    name='django-rest-framework-social-oauth2',
    version=__import__('rest_framework_social_oauth2').__version__,
    description=__import__('rest_framework_social_oauth2').__doc__,
    long_description=open('README.rst').read(),
    author='Philip Garnero',
    author_email='philip.garnero@gmail.com',
    url='https://github.com/PhilipGarnero/django-rest-framework-social-oauth2',
    license='MIT',
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Framework :: Django",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    install_requires=[
        'djangorestframework>=3.10.3',
        'django-oauth-toolkit>=0.12.0',
        'social-auth-app-django>=3.1.0',
    ],
    include_package_data=True,
    zip_safe=False,
)
