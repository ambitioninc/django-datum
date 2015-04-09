from datetime import datetime, timedelta

from django.test import SimpleTestCase, TestCase
from django_dynamic_fixture import G
from freezegun import freeze_time

from datum.models import construct_timedelta, Datum


class ConstructTimedeltaTests(SimpleTestCase):
    def test_construct_timedelta_with_int(self):
        """
        Verify that construct_timedelta will treat an int as a number of seconds and return a timdelta.
        """
        self.assertEquals(timedelta(seconds=60), construct_timedelta(60))

    def test_construct_timedelta_with_timedelta(self):
        """
        Verify that construct_timedelta will simply return a timedelta when given one.
        """
        td = timedelta(hours=1, minutes=30)
        self.assertEquals(td, construct_timedelta(td))

    def test_construct_timedelta_with_other(self):
        """
        Verify that construct_timedelta will raise an exception when given something other than
        an int or timedelta.
        """
        with self.assertRaises(TypeError):
            construct_timedelta('i-am-become-shiva-creater-of-edge-cases')


class DatumTests(TestCase):
    def test_str(self):
        """
        Test the Datum's __str__ method.
        """
        d = G(Datum)
        self.assertEquals('origin:{0} datum_name:{1} note:{2}'.format(
            d.origin, d.name, d.note
        ), str(d))

    def test_creation_with_datum_ttl(self):
        """
        Test that a Datum created with a TLL arg has an appropriately constructed expiration time.
        """
        # Setup scenario
        now = datetime(2015, 4, 8, 12)
        ttl_seconds = 30

        # Run code
        with freeze_time(now):
            d = Datum(ttl=ttl_seconds)

        # Verify expectations
        self.assertEquals(now + timedelta(seconds=ttl_seconds), d.expiration_time)

    def test_creation_without_datum_ttl(self):
        """
        Test that a Datum created without a TLL arg has a null expiration time.
        """
        now = datetime(2015, 4, 8, 12)
        with freeze_time(now):
            d = Datum()

        self.assertEquals(now + timedelta(weeks=8), d.expiration_time)

    def test_clear_expired(self):
        """
        Verify that calling clear_expired removes Datums with an expiration_time in the past.
        """
        # Setup scenario
        creation_time = datetime(2015, 4, 8, 12)
        now = creation_time + timedelta(seconds=30)

        with freeze_time(creation_time):
            d = Datum.objects.create(name='', origin='', ttl=15)

        # Run code
        with freeze_time(now):
            cleared = Datum.objects.clear_expired()

        # Verify expectations
        self.assertEquals(1, cleared)
        self.assertFalse(Datum.objects.filter(id=d.id).exists())

    def test_clear_expired_ignores_unexpired_datums(self):
        """
        Verify that calling clear_expired ignores Datums with an expiration_time in the future.
        """
        # Setup scenario
        creation_time = datetime(2015, 4, 8, 12)
        now = datetime(2015, 4, 8, 12) + timedelta(seconds=30)

        with freeze_time(creation_time):
            d = Datum.objects.create(name='', origin='', ttl=45)

        # Run code
        with freeze_time(now):
            cleared = Datum.objects.clear_expired()

        # Verify expectations
        self.assertEquals(0, cleared)
        self.assertTrue(Datum.objects.filter(id=d.id).exists())

    def test_clear_expired_ignores_default_expiration_times(self):
        """
        Verify that calling clear_expired ignores Datums with a default expiration_time.
        """
        # Setup scenario
        creation_time = datetime(2015, 4, 8, 12)
        now = datetime(2015, 4, 8, 12) + timedelta(seconds=30)

        with freeze_time(creation_time):
            d = Datum.objects.create(name='', origin='')

        # Verify initial expectations
        self.assertEquals(creation_time + timedelta(weeks=8), d.expiration_time)

        # Run code
        with freeze_time(now):
            cleared = Datum.objects.clear_expired()

        # Verify expectations
        self.assertEquals(0, cleared)
        self.assertTrue(Datum.objects.filter(id=d.id).exists())
