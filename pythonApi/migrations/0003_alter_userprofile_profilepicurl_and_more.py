# Generated by Django 4.2.10 on 2024-02-17 23:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pythonApi', '0002_rename_followers_userprofile_followerscount_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='profilePicUrl',
            field=models.CharField(blank=True, default='', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='url',
            field=models.CharField(blank=True, default='', max_length=200, null=True),
        ),
    ]
