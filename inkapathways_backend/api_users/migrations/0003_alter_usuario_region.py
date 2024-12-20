# Generated by Django 5.1.1 on 2024-11-14 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_users', '0002_usuario_fecha_expiracion_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='region',
            field=models.CharField(choices=[('Junin', 'Junín'), ('Lima', 'Lima'), ('Arequipa', 'Arequipa'), ('Cuzco', 'Cuzco'), ('Piura', 'Piura'), ('Trujillo', 'Trujillo'), ('Ica', 'Ica'), ('Callao', 'Callao'), ('Loreto', 'Loreto'), ('Amazonas', 'Amazonas'), ('Puno', 'Puno'), ('Ayacucho', 'Ayacucho'), ('Tacna', 'Tacna'), ('Moquegua', 'Moquegua'), ('Ancash', 'Áncash'), ('Huancavelica', 'Huancavelica'), ('Huanuco', 'Huánuco'), ('Ucayali', 'Ucayali'), ('Madre de Dios', 'Madre de Dios'), ('San Martín', 'San Martín'), ('La Libertad', 'La Libertad'), ('Lambayeque', 'Lambayeque'), ('Cajamarca', 'Cajamarca'), ('Tumbes', 'Tumbes'), ('Apurímac', 'Apurímac'), ('Moquegua', 'Moquegua'), ('Pasco', 'Pasco'), ('Vilcashuamán', 'Vilcashuamán')], max_length=20),
        ),
    ]
