from django.core.management.base import BaseCommand
from django.core.management import call_command
import os

class Command(BaseCommand):
    help = 'Update and compile translation files'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--languages',
            nargs='+',
            default=['fa', 'ar', 'de', 'fr'],
            help='List of language codes to update (default: fa ar de fr)'
        )
        
    def handle(self, *args, **options):
        languages = options['languages']
        
        self.stdout.write(
            self.style.SUCCESS(f'Updating translations for languages: {", ".join(languages)}')
        )
        
        for lang in languages:
            self.stdout.write(f'Processing {lang}...')
            
            # Generate/update message files
            try:
                call_command('makemessages', '-l', lang, verbosity=0)
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Messages updated for {lang}')
                )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'✗ Error updating messages for {lang}: {e}')
                )
                continue
            
        # Compile all message files
        self.stdout.write('Compiling messages...')
        try:
            call_command('compilemessages', verbosity=0)
            self.stdout.write(
                self.style.SUCCESS('✓ All messages compiled successfully')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'✗ Error compiling messages: {e}')
            )
        
        self.stdout.write(
            self.style.SUCCESS('Translation update complete!')
        )