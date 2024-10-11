from django.db import models


class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    correo = models.EmailField(unique=True)
    contraseña_hash = models.CharField(max_length=100)
    region = models.CharField(max_length=10, choices=[
                              ('Junin', 'Junin'), ('Lima', 'Lima')])
    correo_verificado = models.BooleanField(default=False)
    token_verificacion = models.CharField(
        max_length=255, blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'usuarios'  

    def __str__(self):
        return self.correo
    
    @property
    def is_authenticated(self):
        return True  # Indica que este objeto representa un usuario autenticado