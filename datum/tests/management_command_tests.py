from django.test import TestCase
from django.core.management import call_command

from mock import patch

from datum.models import DatumManager


class ClearExpiredDatumsTest(TestCase):
    @patch.object(DatumManager, 'clear_expired', spec_set=True)
    def test_run(self, clear_expired):
        call_command('clear_expired_datums')

        self.assertTrue(clear_expired.called)
