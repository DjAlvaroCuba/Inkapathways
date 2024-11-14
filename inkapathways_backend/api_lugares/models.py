from django.db import models

class Lugar(models.Model):
    provincia = models.TextField()

    def __str__(self):
        return self.provincia

class Mes(models.Model):
    mes = models.CharField(max_length=20)

    def __str__(self):
        return self.mes

class Festividad(models.Model):
    nombre_festividad = models.CharField(max_length=100)
    descripcion_festividad = models.TextField()
    mes = models.ForeignKey(Mes, on_delete=models.CASCADE, null=True, blank=True)
    lugar = models.ForeignKey(Lugar, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.nombre_festividad
