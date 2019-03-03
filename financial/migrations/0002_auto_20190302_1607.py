# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2019-03-02 21:07
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('financial', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveIntegerField()),
                ('date_paid', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AlterField(
            model_name='cost',
            name='type',
            field=models.CharField(choices=[('el', 'Elementor'), ('sh', 'Server Hosting'), ('do', 'Domains'), ('gs', 'GSuite'), ('ot', 'Other')], max_length=2),
        ),
        migrations.AddField(
            model_name='payment',
            name='cost',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='financial.Cost'),
        ),
    ]