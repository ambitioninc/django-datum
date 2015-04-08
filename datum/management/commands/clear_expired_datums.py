from django.core.management.base import BaseCommand

from datum.models import Datum


class Command(BaseCommand):
    help = ('Clear any expired Datums')

    def handle(self, *args, **options):
        clear_count = Datum.objects.clear_expired()

        print('Cleared data: {0}'.format(clear_count))
