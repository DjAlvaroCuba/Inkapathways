from django.db import models


class TablalugaresV2(models.Model):
    region = models.TextField(db_column='REGION', blank=True, null=True)
    provincia = models.TextField(db_column='PROVINCIA', blank=True, null=True)
    distrito = models.TextField(db_column='DISTRITO', blank=True, null=True)
    nombre_del_recurso = models.TextField(
        db_column='NOMBRE DEL RECURSO', blank=True, null=True)
    categoria = models.TextField(db_column='CATEGORIA', blank=True, null=True)
    tipo_de_categoria = models.TextField(
        db_column='TIPO DE CATEGORIA', blank=True, null=True)
    sub_tipo_categoria = models.TextField(
        db_column='SUB TIPO CATEGORIA', blank=True, null=True)
    id_lugar = models.IntegerField(db_column='Id_lugar', primary_key=True)

    class Meta:
        managed = False
        db_table = 'tablalugares_v2'
