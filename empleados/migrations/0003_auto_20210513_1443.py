# Generated by Django 3.2 on 2021-05-13 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('empleados', '0002_auto_20210506_0542'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='empleado',
            name='salario_neto',
        ),
        migrations.AddField(
            model_name='empleado',
            name='edad',
            field=models.CharField(default=' ', max_length=3),
            preserve_default=False,
        ),
    ]
