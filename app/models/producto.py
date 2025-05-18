from django.db import models

class Producto(models.Model):
    NOMBRES = [
        ('aguja_americana_15', 'Aguja Americana 15'),
        ('aguja_americana_14', 'Aguja Americana 14'),
        ('aguja_americana_16', 'Aguja Americana 16'),
        ('aguja_vastago_rl', 'Aguja Vastago RL'),
        ('aguja_vastago_rs', 'Aguja Vastago RS'),
        ('aguja_vastago_rm', 'Aguja Vastago RM'),
        ('labret', 'Labret'),
        ('septum', 'Septum'),
        ('barbell', 'Barbell'),
        ('nostril', 'Nostril'),
        ('aro', 'Aro'),
        ('tinta_negra_oz', 'Tinta Negra Oz'),
        ('tinta_blanca_oz', 'Tinta Blanca Oz'),
        ('rollo_papel_sanitario', 'Rollo Papel Sanitario'),
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
