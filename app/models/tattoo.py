from django.db import models

class Tattoo(models.Model):
    ARTISTS = [
        ('Xavier Verdecie Ramos','xavier verdecie ramos'),
        ('Osmel Medero Rosales','osmel medero rosales')
    ]

    ESTILOS = [
        ('Realismo', 'realismo'),
        ('Tradicional', 'tradicional'),
        ('Neotradicional', 'neotradicional'),
        ('Acuarela', 'acuarela'),
        ('Geométrico', 'geométrico'),
        ('BlackWork','blackwork'),
        ('Trival','trival'),
        ('Sigilo','sigilo')
    ]

    nombre = models.CharField(max_length=30)
    estilo = models.CharField(max_length=255, choices=ESTILOS)
    precio = models.DecimalField(max_digits=5, decimal_places=2, default=1.00)
    foto = models.CharField(max_length=500, null=True, blank=True)
    artista = models.CharField(max_length=30, choices=ARTISTS)
    public = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Tattoo"
        verbose_name_plural = "Tattoos"
