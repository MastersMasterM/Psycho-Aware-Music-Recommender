# Generated by Django 5.0.6 on 2024-07-08 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inferenceengine', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='instrumentalness',
            field=models.JSONField(blank=True, default=list, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='key_signatures',
            field=models.JSONField(blank=True, default=list, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='tempo',
            field=models.JSONField(blank=True, default=list, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='valence',
            field=models.JSONField(blank=True, default=list, null=True),
        ),
    ]
