from rest_framework import viewsets, status
from rest_framework.response import Response
from django.db import transaction
from datetime import date
from app.api.permissions.authentication import CsrfExemptSessionAuthentication
from app.api.permissions.permissions import IsSuperuserOrTatuadorOrPerforador
from app.api.serializers.reporte_uso_materialSerializer import Reporte_Uso_MaterialSerializer
from app.models.reporte_uso_material import Reporte_Uso_Material
from app.models.producto import Producto


class Reporte_Uso_MaterialViewSet(viewsets.ModelViewSet):
    queryset = Reporte_Uso_Material.objects.all()
    serializer_class = Reporte_Uso_MaterialSerializer
    permission_classes = [IsSuperuserOrTatuadorOrPerforador]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        material_nombre = serializer.validated_data['material_nombre']
        cantidad = serializer.validated_data['cantidad']

        with transaction.atomic():
            materiales = Producto.objects.filter(
                nombre=material_nombre,
                disponible=True,
                cat="materiales"
            ).order_by('id')[:cantidad] 


            if len(materiales) < cantidad:
                return Response(
                    {"error": f"Solo hay {len(materiales)} unidades disponibles"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            for material in materiales:
                material.disponible = False

            Producto.objects.bulk_update(materiales, ['disponible'])

            reporte = Reporte_Uso_Material.objects.create(
                cantidad=cantidad,
                fecha=date.today()
            )
            reporte.materiales.set(materiales) 

        return Response(Reporte_Uso_MaterialSerializer(reporte).data, status=status.HTTP_201_CREATED)