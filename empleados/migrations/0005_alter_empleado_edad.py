# Generated by Django 3.2 on 2021-05-13 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('empleados', '0004_alter_empleado_edad'),
    ]

    operations = [
        migrations.AlterField(
            model_name='empleado',
            name='edad',
            field=models.CharField(blank=True, max_length=3, null=True),
        ),
    ]
