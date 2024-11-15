from django.db import models
# Create your models here.
from api_users.models import Usuario  
class Pregunta(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='preguntas')  # Referencia al modelo Usuario
    pregunta = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'preguntas'  

    def __str__(self):
        return self.pregunta
    
class Respuesta(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='respuestas')
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE, related_name='respuestas')
    respuesta = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'respuestas'  # Especifica el nombre de la tabla en la base de datos

    def __str__(self):
        return self.respuesta