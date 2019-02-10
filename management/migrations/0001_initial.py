# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2019-02-10 14:53
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Cost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('el', 'Elementor'), ('sh', 'Server Hosting'), ('do', 'do'), ('gs', 'gs')], max_length=2)),
                ('price', models.PositiveIntegerField()),
                ('client_payment', models.IntegerField()),
                ('first_paymnet', models.DateTimeField()),
                ('payment_period', models.CharField(choices=[('wk', 'Bi-weekly'), ('mo', 'Monthly'), ('an', 'Annualy')], max_length=2)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='management.Client')),
            ],
        ),
    ]
