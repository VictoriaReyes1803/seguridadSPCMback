# Generated by Django 5.1.1 on 2024-11-08 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spcmapp', '0008_user_profile_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='apellido_materno',
            field=models.CharField(max_length=100, null=True),
        ),
    ]