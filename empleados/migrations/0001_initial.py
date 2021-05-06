# Generated by Django 3.2 on 2021-05-06 04:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Empleado',
            fields=[
                ('id_empleado', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=15)),
                ('apellido', models.CharField(max_length=15)),
                ('salario', models.DecimalField(decimal_places=2, max_digits=7)),
                ('salario_libre_imp', models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True)),
                ('impuestos', models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True)),
                ('aportes_seg_soc', models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True)),
                ('salario_neto', models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True)),
            ],
        ),
    ]