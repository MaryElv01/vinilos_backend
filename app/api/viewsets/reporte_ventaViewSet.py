from rest_framework import viewsets, status
from rest_framework.response import Response
from django.db import transaction
from datetime import date
from app.api.permissions.authentication import CsrfExemptSessionAuthentication
from app.api.permissions.permissions import IsSuperuserOrPerforador
from app.models import Reporte_Venta, Producto
from app.api.serializers import Reporte_VentaSerializer

class Reporte_VentaViewSet(viewsets.ModelViewSet):
    queryset = Reporte_Venta.objects.all()
    serializer_class = Reporte_VentaSerializer
    permission_classes = [IsSuperuserOrPerforador]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        producto_nombre = serializer.validated_data['producto_nombre']
        cantidad = serializer.validated_data['cantidad']
        cliente = serializer.validated_data['cliente']

        with transaction.atomic():
            productos = Producto.objects.filter(
                nombre=producto_nombre,
                disponible=True
            ).order_by('id')[:cantidad] 


            if len(productos) < cantidad:
                return Response(
                    {"error": f"Solo hay {len(productos)} unidades disponibles"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            aporte = 0
            for producto in productos:
                producto.disponible = False
                producto.fecha_v = date.today()
                aporte += producto.precio

            Producto.objects.bulk_update(productos, ['disponible', 'fecha_v'])

            reporte = Reporte_Venta.objects.create(
                cliente=cliente,
                cantidad=cantidad,
                aporte=int(aporte),
                fecha=date.today()
            )
            reporte.productos.set(productos) 

        return Response(Reporte_VentaSerializer(reporte).data, status=status.HTTP_201_CREATED)