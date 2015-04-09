# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Datum',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('expiration_time', models.DateTimeField(default=None, null=True, blank=True)),
                ('origin', models.CharField(max_length=64)),
                ('name', models.CharField(max_length=64)),
                ('note', jsonfield.fields.JSONField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
