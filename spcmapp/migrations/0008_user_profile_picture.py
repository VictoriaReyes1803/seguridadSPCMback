# Generated by Django 5.1.1 on 2024-11-06 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spcmapp', '0007_user_reset_token'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='profile_pictures/'),
        ),
    ]
