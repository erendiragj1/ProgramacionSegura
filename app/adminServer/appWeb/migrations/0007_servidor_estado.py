# Generated by Django 3.0.5 on 2020-06-04 18:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appWeb', '0006_auto_20200508_1938'),
    ]

    operations = [
        migrations.AddField(
            model_name='servidor',
            name='estado',
            field=models.BooleanField(default=True, verbose_name='Activo/Inactivo'),
        ),
    ]