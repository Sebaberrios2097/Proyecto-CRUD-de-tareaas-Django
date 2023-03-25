from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Tasks(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)
    completado = models.BooleanField(default=False, blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    important = models.BooleanField(default=False)
    fecha_completado = models.DateTimeField(blank=True, null=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.titulo + ' | ' + str(self.usuario)
    
    class Meta:
        db_table = 'Tasks'
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'
        ordering = ['-fecha_creacion']