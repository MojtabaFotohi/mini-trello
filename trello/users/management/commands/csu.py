from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import IntegrityError

class Command(BaseCommand):
    help = 'Creates a superuser with predefined credentials: username=admin, email=admin@gmail.com, password=admin'

    def handle(self, *args, **options):
        User = get_user_model()
        username = 'admin'
        email = 'admin@gmail.com'
        password = 'admin'

        try:
            if User.objects.filter(username=username).exists():
                self.stdout.write(self.style.ERROR(f'Superuser with username "{username}" already exists.'))
                return

            user = User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            self.stdout.write(self.style.SUCCESS(f'Successfully created superuser: {username}'))
        except IntegrityError:
            self.stdout.write(self.style.ERROR(f'Error: User with email "{email}" already exists.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error creating superuser: {str(e)}'))
