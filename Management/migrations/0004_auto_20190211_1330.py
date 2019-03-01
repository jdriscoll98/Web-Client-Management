# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2019-02-11 18:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0003_auto_20190211_1321'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cost',
            old_name='first_payment',
            new_name='last_payment_date',
        ),
        migrations.RemoveField(
            model_name='cost',
            name='next_payment',
        ),
        migrations.AddField(
            model_name='cost',
            name='payment_period',
            field=models.CharField(choices=[('wk', 'Bi-weekly'), ('mo', 'Monthly'), ('an', 'Annualy')], default='wk', max_length=2),
        ),
    ]