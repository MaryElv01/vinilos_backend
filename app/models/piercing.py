from django.db import models

class Piercing(models.Model):
    UBIS = [
        ('Lóbulo', 'lobulo'),
        ('Helix', 'helix'),
        ('Tragus', 'tragus'),
        ('Antitragus', 'antitragus'),
        ('Daith', 'daith'),
        ('Rook', 'rook'),
        ('Conch', 'conch'),
        ('Snug', 'snug'),
        ('Industrial', 'industrial'),
        ('Septum', 'septum'),
        ('Fosa nasal', 'fosa nasal'),
        ('Labret', 'labret'),
        ('Medusa', 'medusa'),
        ('Ceja', 'ceja'),
        ('Ombligo', 'ombligo'),
        ('Pezón', 'pezon'),
        ('Surface', 'surface'),
        ('Microdermal', 'microdermal')  
    ]

    nombre = models.CharField(max_length=30)
    ubi = models.CharField(max_length=255, choices=UBIS)
    foto = models.CharField(max_length=500, null=True, blank=True)
    precio = models.IntegerField(default=250)
    public = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Piercing"
        verbose_name_plural = "Piercings"
