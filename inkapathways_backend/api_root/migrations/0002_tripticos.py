# Generated by Django 5.1.1 on 2024-12-09 22:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_root', '0001_initial'),
        ('api_users', '0006_rename_region_usuario_lugar_procedencia'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tripticos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_salida', models.DateField()),
                ('fecha_retorno', models.DateField()),
                ('lugares_turisticos', models.TextField()),
                ('idioma', models.TextField()),
                ('hotel', models.TextField()),
                ('adultos', models.IntegerField()),
                ('infantes', models.IntegerField()),
                ('presupuesto', models.DecimalField(decimal_places=2, max_digits=10)),
                ('transporte', models.TextField()),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('respuestacomida', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api_root.respuesta')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api_users.usuario')),
            ],
            options={
                'db_table': 'tripticos',
            },
        ),
    ]