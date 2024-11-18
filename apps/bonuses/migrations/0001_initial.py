# Generated by Django 5.1.3 on 2024-11-18 09:06

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BonusMoney',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bonus_money', models.IntegerField(default=0)),
                ('card_number', models.CharField(max_length=16)),
                ('user', models.ForeignKey(limit_choices_to={'role__in': ['admin', 'supplier']}, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
