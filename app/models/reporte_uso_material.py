from datetime import date
from django.db import models

from app.models.producto import Producto

class Reporte_Uso_Material(models.Model):
    fecha = models.DateField(default=date.today())
    materiales = models.ManyToManyField(Producto)
    cantidad = models.IntegerField(default=1)

    class Meta:
        verbose_name = "Reporte_Uso_Material"
        verbose_name_plural = "Reportes_Uso_Material"