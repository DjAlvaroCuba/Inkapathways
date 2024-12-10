from django.db import models
# Create your models here.
from api_users.models import Usuario  
class Pregunta(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='preguntas')  
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
        db_table = 'respuestas'  

    def __str__(self):
        return self.respuesta
    
class Tripticos(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha_salida = models.DateField()
    fecha_retorno = models.DateField()
    lugares_turisticos = models.TextField()
    idioma = models.TextField()
    hotel = models.TextField()
    adultos = models.IntegerField()
    infantes = models.IntegerField() 
    presupuesto = models.DecimalField(max_digits=10, decimal_places=2)  # Usamos DecimalField para el presupuesto
    transporte = models.TextField()
    comidas = models.ManyToManyField(Respuesta, related_name='tripticos_comidas') 
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'tripticos'

    def __str__(self):
        return f"Triptico de {self.usuario}"

    
