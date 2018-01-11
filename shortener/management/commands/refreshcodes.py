from django.core.management.base import BaseCommand, CommandError
from shortener.models import Srturl

class Command(BaseCommand):
    help = 'Refreshes all Srturl shortcodes'

    def add_arguments(self, parser):
        parser.add_argument('--items', type=int)

    def handle(self, *args, **options):
        return Srturl.objects.refresh_shortcodes(items=options['items'])