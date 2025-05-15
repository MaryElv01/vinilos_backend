from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class Reporte_Finanza(models.Model):
    INCOME = 'ingreso'
    EXPENSE = 'gasto'

    TYPE_CHOICES = [
        (INCOME,  'Ingreso'),
        (EXPENSE, 'Gasto'),
    ]

    date        = models.DateTimeField(auto_now_add=True)
    transaction_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    description = models.CharField(max_length=255)
    amount      = models.DecimalField(max_digits=10, decimal_places=2)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id    = models.PositiveIntegerField(null=True, blank=True)
    source_obj   = GenericForeignKey('content_type', 'object_id')
