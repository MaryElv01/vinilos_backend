from datetime import date
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from app.api.permissions.authentication import CsrfExemptSessionAuthentication
from app.models import Reporte_Abastecimiento, Producto
from app.api.serializers import Reporte_AbastecimientoSerializer, VenderProductoSerializer

class Reporte_AbastecimientoViewSet(viewsets.ModelViewSet):
    queryset = Reporte_Abastecimiento.objects.all()
    serializer_class = Reporte_AbastecimientoSerializer
    permission_classes = [permissions.IsAdminUser]

    def perform_update(self, serializer):
        instance = serializer.save()
        if instance.estado == 'Entregado':
            if not instance.fecha_llegada:
                instance.fecha_llegada = date.today()
                instance.save()
            
            productos = Producto.objects.filter(itempedido__pedido=instance)
            productos.update(disponible=True)