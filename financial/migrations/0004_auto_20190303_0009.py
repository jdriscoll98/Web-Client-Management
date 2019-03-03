# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2019-03-03 05:09
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0006_client_amount_owed'),
        ('financial', '0003_auto_20190302_2310'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cost',
            name='other',
        ),
        migrations.AddField(
            model_name='cost',
            name='project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='management.Project'),
        ),
        migrations.AlterField(
            model_name='cost',
            name='type',
            field=models.CharField(choices=[('el', 'Elementor'), ('sh', 'Server Hosting'), ('do', 'Domains'), ('pj', 'Project')], max_length=2),
        ),
    ]
