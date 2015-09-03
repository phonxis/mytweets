# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserFollowers',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('count', models.IntegerField(default=1)),
                ('followers', models.ManyToManyField(related_name='followers', to='user_profile.User')),
                ('user', models.ForeignKey(to='user_profile.User', unique=True)),
            ],
        ),
    ]
