# Generated by Django 3.1.7 on 2021-03-08 02:19

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('orig_link', models.URLField()),
                ('domain_name', models.CharField(max_length=100)),
                ('random_sequence', models.CharField(max_length=8, unique=True)),
                ('creation_date', models.DateTimeField(default=datetime.datetime.utcnow)),
                ('life_time_end', models.DateTimeField(default=datetime.datetime(9999, 12, 31, 23, 59, 59, 999999))),
                ('link_tag', models.CharField(max_length=32)),
                ('link_owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Link',
                'verbose_name_plural': 'Links',
            },
        ),
        migrations.CreateModel(
            name='Transitions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trans_time', models.DateTimeField()),
                ('link_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ShortenYourLink.link')),
                ('owner_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Transition',
                'verbose_name_plural': 'Transitions',
            },
        ),
    ]
