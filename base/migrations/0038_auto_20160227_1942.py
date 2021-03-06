# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('base', '0037_gamerequest_game_config'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submit',
            name='status',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='status',
                                                   choices=[(0, 'waiting'), (1, 'queued'), (2, 'compiling'),
                                                            (3, 'compiled'), (4, 'failed')]),
        ),
    ]
