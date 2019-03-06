# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-03-06 05:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0004_project_amount'),
        ('financial', '0004_auto_20190305_2348'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='clientcost',
            name='payment_period',
        ),
        migrations.RemoveField(
            model_name='companycost',
            name='payment_period',
        ),
        migrations.AddField(
            model_name='costtype',
            name='payment_period',
            field=models.CharField(choices=[('ot', 'One Time'), ('wk', 'Bi-weekly'), ('mo', 'Monthly'), ('an', 'Annualy')], default='ot', max_length=2),
        ),
        migrations.AlterField(
            model_name='costtype',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterUniqueTogether(
            name='costtype',
            unique_together=set([('name', 'company')]),
        ),
        migrations.AlterUniqueTogether(
            name='service',
            unique_together=set([('name', 'company')]),
        ),
    ]
