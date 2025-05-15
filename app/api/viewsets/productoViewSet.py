from rest_framework.decorators import action
from django.db.models import Count, Sum, Q, F
from rest_framework import viewsets, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from urllib.parse import urlparse
import os
import cloudinary.uploader

from app.api.permissions.authentication import CsrfExemptSessionAuthentication
from app.api.permissions.permissions import IsSuperuserOrPerforador
from ...models import Producto
from ..serializers import ProductoSerializer

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsSuperuserOrPerforador]
    authentication_classes = [CsrfExemptSessionAuthentication]

    @action(detail=False, methods=['get'], url_path='piercings_venta')
    def piercings_venta(self, request):
        """
        Devuelve una lista de piercings disponibles, un solo objeto por cada nombre.
        GET /api/producto/piercings_venta/
        """
        qs = Producto.objects.filter(cat='piercing', disponible=True).order_by('nombre', 'id')
        # Usamos un dict para quedarnos con la primera instancia de cada nombre
        únicos = {}
        for p in qs:
            if p.nombre not in únicos:
                únicos[p.nombre] = p

        serializer = ProductoSerializer(únicos.values(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def inventario(self, request):
        # 1) Total de productos (todas las filas)
        total_productos = Producto.objects.filter(disponible=True).count()

        # 2) Valor del inventario = suma de costo de las unidades disponibles
        valor = (
            Producto.objects
            .filter(disponible=True)
            .aggregate(valor_inv=Sum('costo'))
        )['valor_inv'] or 0

        # 3) Conteo por nombre de las unidades con disponible=True
        qs_por_nombre = (
            Producto.objects
            .values('nombre')
            .annotate(stock=Count('id', filter=Q(disponible=True)))
        )
        # aquí podrías tener un dict de mínimos por nombre:
        MINIMOS = {
            'aguja_americana_14': 5,
            'labret': 10,
            # …etc…
        }
        # 4) Productos con stock bajo (aplico el umbral)
        stock_bajo = sum(
            1 for fila in qs_por_nombre
            if fila['stock'] < MINIMOS.get(fila['nombre'], 0)
        )

        return Response({
            'total_productos': total_productos,
            'valor_inventario': valor,
            'productos_stock_bajo': stock_bajo,
        })

    @action(detail=False, methods=['get'])
    def resumen(self, request):
        STOCK_MIN = {
            'aguja_americana_14': 5,
            'labret': 8,
            'industrial': 4,
            'aguja_rl5': 10,
            'aguja_rl7': 10,
            'tinta_negra_oz': 20,
            'paquete_toallitas_humedas': 6,
        }

        qs = (
            Producto.objects
            .values('nombre', 'cat')
            .annotate(
                stock=Count('id', filter=Q(disponible=True)),
                precio_compra_total=Sum(
                    F('costo'),
                    filter=Q(disponible=True)
                )
            )
        )

        data = []
        for row in qs:
            row['stock_minimo'] = STOCK_MIN.get(row['nombre'], 0)
            data.append(row)

        return Response(data)

    def perform_cloudinary_upload(self, file):
        result = cloudinary.uploader.upload(
            file,
            folder='vinilos/ventas/'
        )
        return result.get('secure_url')

    def get_public_id_from_url(self, url):
        path = urlparse(url).path.lstrip('/')
        public_id, _ = os.path.splitext(path)
        return public_id

    def create(self, request, *args, **kwargs):
        image_file = request.FILES.get('foto')
        if image_file:
            url = self.perform_cloudinary_upload(image_file)
            request.data['foto'] = url

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            prod = serializer.save()
            return Response(self.get_serializer(prod).data, status=status.HTTP_201_CREATED)
        return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.foto:
            public_id = self.get_public_id_from_url(instance.foto.url)
            cloudinary.uploader.destroy(public_id)
        instance.delete()
        return Response({"message": "Producto eliminado"}, status=status.HTTP_204_NO_CONTENT)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        old_url = instance.foto.url if instance.foto else None

        image_file = request.FILES.get('foto')
        if image_file:
            if old_url:
                public_id = self.get_public_id_from_url(old_url)
                cloudinary.uploader.destroy(public_id)
            url = self.perform_cloudinary_upload(image_file)
            request.data['foto'] = url

        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid():
            prod = serializer.save()
            return Response(self.get_serializer(prod).data, status=status.HTTP_200_OK)
        return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        old_url = instance.foto.url if instance.foto else None

        image_file = request.FILES.get('foto')
        if image_file:
            if old_url:
                public_id = self.get_public_id_from_url(old_url)
                cloudinary.uploader.destroy(public_id)
            url = self.perform_cloudinary_upload(image_file)
            request.data['foto'] = url

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            prod = serializer.save()
            return Response(self.get_serializer(prod).data, status=status.HTTP_200_OK)
        return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
