# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_auto_20141104_0539'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='level',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
