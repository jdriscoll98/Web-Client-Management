# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2019-02-11 02:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='client',
            old_name='client',
            new_name='name',
        ),
        migrations.AlterField(
            model_name='cost',
            name='type',
            field=models.CharField(choices=[('el', 'Elementor'), ('sh', 'Server_Hosting'), ('do', 'Domains'), ('gs', 'GSuite')], max_length=2),
        ),
    ]
