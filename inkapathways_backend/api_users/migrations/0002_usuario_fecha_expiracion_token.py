# Generated by Django 5.1.1 on 2024-10-31 05:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='fecha_expiracion_token',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
