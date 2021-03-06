# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_product_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='raters',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='product',
            name='total_rating',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
