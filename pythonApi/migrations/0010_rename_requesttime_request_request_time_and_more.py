# Generated by Django 4.2.10 on 2024-02-18 22:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pythonApi', '0009_rename_followerscount_userprofile_followers_count_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='request',
            old_name='requestTime',
            new_name='request_time',
        ),
        migrations.AddField(
            model_name='request',
            name='success',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='request',
            name='username',
            field=models.CharField(blank=True, default='', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='username',
            field=models.CharField(blank=True, default='', max_length=100, null=True),
        ),
    ]