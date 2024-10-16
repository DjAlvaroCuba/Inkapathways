# Generated by Django 5.1.1 on 2024-10-14 00:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TablalugaresV2',
            fields=[
                ('region', models.TextField(blank=True, db_column='REGION', null=True)),
                ('provincia', models.TextField(blank=True, db_column='PROVINCIA', null=True)),
                ('distrito', models.TextField(blank=True, db_column='DISTRITO', null=True)),
                ('nombre_del_recurso', models.TextField(blank=True, db_column='NOMBRE DEL RECURSO', null=True)),
                ('categoria', models.TextField(blank=True, db_column='CATEGORIA', null=True)),
                ('tipo_de_categoria', models.TextField(blank=True, db_column='TIPO DE CATEGORIA', null=True)),
                ('sub_tipo_categoria', models.TextField(blank=True, db_column='SUB TIPO CATEGORIA', null=True)),
                ('id_lugar', models.IntegerField(db_column='Id_lugar', primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'tablalugares_v2',
                'managed': False,
            },
        ),
    ]