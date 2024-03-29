# Generated by Django 4.2.10 on 2024-02-18 23:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pythonApi', '0011_alter_userprofile_profile_pic_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='media',
            name='comments',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='media',
            name='date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='media',
            name='likes',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
