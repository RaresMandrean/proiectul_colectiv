# Generated by Django 2.2.7 on 2020-01-12 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventix', '0002_seat'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='poster',
            field=models.ImageField(blank=True, null=True, upload_to='event_posters'),
        ),
    ]
