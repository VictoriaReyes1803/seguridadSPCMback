# Generated by Django 5.1.1 on 2024-11-11 19:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spcmapp', '0009_alter_user_apellido_materno'),
    ]

    operations = [
        migrations.AddField(
            model_name='maquina',
            name='Formato',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='producto_maquina',
            name='Formato',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]