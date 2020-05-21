# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-05-21 03:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import gameplay.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Board',
            fields=[
                ('turn', models.CharField(choices=[(b'BLUEAGENT', 'BA'), (b'BLUEMASTER', 'BM'), (b'REDAGENT', 'RA'), (b'REDMASTER', 'RM')], default=gameplay.models.Turn('RM'), max_length=10)),
                ('status', models.CharField(choices=[(b'BLUEWIN', 'BW'), (b'DRAW', 'DRAW'), (b'INPROGRESS', 'IP'), (b'REDWIN', 'RW')], default=gameplay.models.BoardStatus('IP'), max_length=10)),
                ('bluescore', models.IntegerField(default=0)),
                ('redscore', models.IntegerField(default=0)),
                ('num_clues', models.IntegerField(default=-1)),
                ('num_clicks', models.IntegerField(default=-1)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(default=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False), max_length=128)),
                ('clue', models.CharField(default='', max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word', models.CharField(max_length=128)),
                ('status', models.CharField(choices=[(b'CLOSED', 'C'), (b'OPEN', 'O')], max_length=10)),
                ('type', models.CharField(choices=[(b'BLUE', 'B'), (b'RED', 'R'), (b'WHITE', 'W')], max_length=10)),
                ('board', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gameplay.Board')),
            ],
        ),
    ]
