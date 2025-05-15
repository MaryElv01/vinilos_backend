from django.db import models

class Producto(models.Model):
    NOMBRES = [
        ('aguja_americana_14', 'Aguja Americana 14'),
        ('labret', 'Labret'),
        ('industrial', 'Industrial'),
        ('aguja_rl5', 'Aguja RL5'),
        ('aguja_rl7', 'Aguja RL7'),
        ('tinta_negra_oz', 'Tinta Negra Oz'),
        ('paquete_toallitas_humedas', 'Paquete Toallitas Humedas')
    ]

    CATEGORIA = [
        ('piercing', 'Piercing'),
        ('cuidado', 'Cuidado'),
        ('materiales', 'Materiales')
    ]

    nombre = models.CharField(max_length=50, choices=NOMBRES)
    cat = models.CharField(max_length=20, choices=CATEGORIA)
    costo = models.DecimalField(max_digits=5, decimal_places=2, default=1.00)
    precio = models.DecimalField(max_digits=5, decimal_places=2, default=1.00, null=True, blank=True)
    foto = models.CharField(max_length=500, null=True, blank=True)
    fecha_v = models.DateField(default=None, null=True, blank=True)
    disponible = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
