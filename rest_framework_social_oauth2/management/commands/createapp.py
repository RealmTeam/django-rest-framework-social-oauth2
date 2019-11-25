from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from oauth2_provider.models import Application
from oauth2_provider.generators import generate_client_id, generate_client_secret


class Command(BaseCommand):
    help = "Create a Django OAuth Toolkit application (an existing admin is required)"

    def add_arguments(self, parser):
        parser.add_argument(
            "-ci", "--client_id",
            help="Client ID (recommeded 40 characters long)"
        )
        parser.add_argument(
            "-cs", "--client_secret",
            help="Client Secret (recommeded 128 characters long)"
        )
        parser.add_argument(
            "-n", "--name",
            help="Name for the application"
        )

    def handle(self, *args, **options):
        new_application = Application(
            user= User.objects.filter(is_superuser=True)[0],
            client_type="confidential",
            authorization_grant_type="password",
            name=options["name"] or "socialauth_application",
            client_id=options["client_id"] or generate_client_id(),
            client_secret=options["client_secret"] or generate_client_secret(),
        )
        new_application.save()
