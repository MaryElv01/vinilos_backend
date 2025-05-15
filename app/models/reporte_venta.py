from datetime import date
from django.db import models

from app.models.producto import Producto

class Reporte_Venta(models.Model):
    fecha = models.DateField(default=date.today)
    productos = models.ManyToManyField(Producto)
    cliente = models.CharField(max_length=255)
    cantidad = models.IntegerField(default=1)
    aporte = models.IntegerField(null=True, blank=True)

    class Meta:
        verbose_name = "Reporte_Venta"
        verbose_name_plural = "Reportes_Venta"