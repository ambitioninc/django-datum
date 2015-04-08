from datetime import datetime, timedelta
import six

from django.db import models
from jsonfield import JSONField


class DatumManager(models.Manager):
    """
    A model manager for Datum records.
    Provides various management capabilities, like deleting expired Datum records.
    """
    def clear_expired(self):
        expired_set = self.filter(expiration_time__isnull=False, expiration_time__lte=datetime.utcnow())

        expired_set_count = expired_set.count()

        expired_set.delete()

        return expired_set_count


def construct_timedelta(ttl):
    if type(ttl) is int:
        return timedelta(seconds=ttl)
    elif type(ttl) is timedelta:
        return ttl
    else:
        raise TypeError('ttl must be integer or timedelta')


@six.python_2_unicode_compatible
class Datum(models.Model):
    """
    A generic way to track notes that your system should keep track of.
    Think of it as internal, machine accessible, logging for your application.
    """
    # When was this datum added to the database
    created_time = models.DateTimeField(auto_now_add=True)

    # When this datum should be removed from the database
    expiration_time = models.DateTimeField(null=True, blank=True, default=None)

    # Origin of this datum; ie, what piece of software created it
    origin = models.CharField(max_length=64)
    name = models.CharField(max_length=64)

    note = JSONField(null=True, blank=True)

    objects = DatumManager()

    def __init__(self, *args, **kwargs):
        ttl = kwargs.pop('ttl', timedelta(weeks=8))

        kwargs['expiration_time'] = datetime.utcnow() + construct_timedelta(ttl)

        super(Datum, self).__init__(*args, **kwargs)

    def __str__(self):
        return 'origin:{0} datum_name:{1} note:{2}'.format(self.origin, self.name, self.note)
