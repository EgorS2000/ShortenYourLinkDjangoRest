# Generated by Django 3.1.7 on 2021-03-20 01:09

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ShortenYourLink', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='link',
            name='creation_date',
            field=models.DateTimeField(default=datetime.datetime.utcnow, help_text='Short link creation time', verbose_name='creation_date'),
        ),
        migrations.AlterField(
            model_name='link',
            name='domain_name',
            field=models.CharField(help_text='Domain name of original link', max_length=100, verbose_name='domain_name'),
        ),
        migrations.AlterField(
            model_name='link',
            name='life_time_end',
            field=models.DateTimeField(default=datetime.datetime(9999, 12, 31, 23, 59, 59, 999999), help_text='Time until which the link will be liquid', verbose_name='life_time_end'),
        ),
        migrations.AlterField(
            model_name='link',
            name='link_owner',
            field=models.ForeignKey(help_text="Link owner's id", on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='link_owner'),
        ),
        migrations.AlterField(
            model_name='link',
            name='link_tag',
            field=models.CharField(help_text="Link's tag", max_length=32, verbose_name='link_tag'),
        ),
        migrations.AlterField(
            model_name='link',
            name='orig_link',
            field=models.URLField(help_text='Original link', verbose_name='orig_link'),
        ),
        migrations.AlterField(
            model_name='link',
            name='random_sequence',
            field=models.CharField(help_text='Short link identifier', max_length=8, unique=True, verbose_name='random_sequence'),
        ),
        migrations.AlterField(
            model_name='transitions',
            name='link_id',
            field=models.ForeignKey(help_text='Identifier of link', on_delete=django.db.models.deletion.CASCADE, to='ShortenYourLink.link', verbose_name='link_id'),
        ),
        migrations.AlterField(
            model_name='transitions',
            name='owner_id',
            field=models.ForeignKey(help_text='Owner of this link', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='owner_id'),
        ),
        migrations.AlterField(
            model_name='transitions',
            name='trans_time',
            field=models.DateTimeField(help_text='Transition time', verbose_name='trans_time'),
        ),
    ]
