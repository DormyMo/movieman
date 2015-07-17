# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Alia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Alia', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Areas',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('area', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Director',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('director', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Genres',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('genreName', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.CharField(max_length=100, primary_key=True, serialize=False, unique=True)),
                ('title', models.CharField(max_length=200, null=True)),
                ('year', models.IntegerField(default=0)),
                ('type', models.CharField(max_length=200, null=True)),
                ('imdbId', models.CharField(default=0, max_length=200)),
                ('imdbScore', models.FloatField(default=0.0, null=True)),
                ('introduction', models.TextField(null=True)),
                ('runtime', models.IntegerField(default=0)),
                ('poster', models.CharField(max_length=200, null=True)),
                ('download', models.CharField(max_length=400, null=True)),
                ('site', models.CharField(max_length=20, null=True)),
                ('siteId', models.CharField(max_length=100, null=True)),
                ('siteScore', models.FloatField(default=0.0, null=True)),
                ('siteStars', models.CharField(max_length=30)),
                ('siteVoteCount', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='PubTime',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pubTime', models.CharField(max_length=100)),
                ('movie', models.ForeignKey(to='common.Movie')),
            ],
        ),
        migrations.AddField(
            model_name='language',
            name='movie',
            field=models.ForeignKey(to='common.Movie'),
        ),
        migrations.AddField(
            model_name='genres',
            name='movie',
            field=models.ForeignKey(to='common.Movie'),
        ),
        migrations.AddField(
            model_name='director',
            name='movie',
            field=models.ForeignKey(to='common.Movie'),
        ),
        migrations.AddField(
            model_name='areas',
            name='movie',
            field=models.ForeignKey(to='common.Movie'),
        ),
        migrations.AddField(
            model_name='alia',
            name='movie',
            field=models.ForeignKey(to='common.Movie'),
        ),
    ]
