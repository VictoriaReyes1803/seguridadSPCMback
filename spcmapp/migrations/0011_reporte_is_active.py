# Generated by Django 5.1.1 on 2024-11-19 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spcmapp', '0010_maquina_formato_producto_maquina_formato'),
    ]

    operations = [
        migrations.AddField(
            model_name='reporte',
            name='is_active',
            field=models.BooleanField(blank=True, default=True, null=True),
        ),
    ]
