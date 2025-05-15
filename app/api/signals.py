from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from ..models import Reporte_Abastecimiento, Reporte_Venta, Reporte_Finanza, Tattoo, Piercing

@receiver(post_save, sender=Reporte_Abastecimiento)
def create_abastecimiento_transaction(sender, instance, created, **kwargs):
    if created or instance.estado == 'Entregado':
        Reporte_Finanza.objects.create(
            transaction_type=Reporte_Finanza.EXPENSE,
            description=f"Abastecimiento: {instance.nombre}",
            amount=instance.costoTot or 0,
            content_type=ContentType.objects.get_for_model(instance),
            object_id=instance.id
        )

@receiver(post_save, sender=Reporte_Venta)
def create_venta_transaction(sender, instance, created, **kwargs):
    if created:
        Reporte_Finanza.objects.create(
            transaction_type=Reporte_Finanza.INCOME,
            description=f"Venta: {instance.cliente}",
            amount=instance.aporte or 0,
            content_type=ContentType.objects.get_for_model(instance),
            object_id=instance.id
        )

@receiver(post_save, sender=Tattoo)
def create_tattoo_transaction(sender, instance, created, **kwargs):
    # solo al crear el registro del tatuaje
    print("tatt")
    if created:
        Reporte_Finanza.objects.create(
            transaction_type=Reporte_Finanza.INCOME,
            description=f"Tatuaje: {instance.nombre} por {instance.artista}",
            amount=instance.precio or 0,
            content_type=ContentType.objects.get_for_model(instance),
            object_id=instance.id
        )

@receiver(post_save, sender=Piercing)
def create_piercing_transaction(sender, instance, created, **kwargs):
    print("pierc")
    # solo al crear el registro del piercing
    if created:
        Reporte_Finanza.objects.create(
            transaction_type=Reporte_Finanza.INCOME,
            description=f"Piercing: {instance.nombre} en {instance.ubi}",
            amount=instance.precio or 0,
            content_type=ContentType.objects.get_for_model(instance),
            object_id=instance.id
        )