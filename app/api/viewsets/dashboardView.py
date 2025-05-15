# app/api/views/dashboard.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.timezone import now
from django.db.models import Sum

from app.models import Producto, Tattoo, Reporte_Venta, Reporte_Abastecimiento
from app.models import Reporte_Finanza
from app.api.permissions import IsSuperuserOrTatuadorOrPerforador

class DashboardAPIView(APIView):
    permission_classes = [IsSuperuserOrTatuadorOrPerforador]

    def get(self, request):
        hoy = now().date()

        # 1) Piercings en Inventario (Producto.cat='piercing' + disponible)
        piercings_invent = Producto.objects.filter(cat='piercing', disponible=True).count()

        # 2) Tatuajes Realizados (Tattoo.public=True)
        tatuajes_realizados = Tattoo.objects.filter(public=True).count()

        # 3) Piercings Vendidos (Reporte_Venta.productos__cat='piercing')
        piercings_vendidos = (
            Reporte_Venta.objects
            .filter(productos__cat='piercing')
            .aggregate(total=Sum('cantidad'))['total'] or 0
        )

        # 4) Productos en Inventario (total disponibles)
        productos_inventario = Producto.objects.filter(disponible=True).count()

        # 5) Actividad Reciente: últimos 5 FinancialTransaction
        transacciones = Reporte_Finanza.objects.order_by('-date')[:5]
        eventos = []
        for tr in transacciones:
            dias = (hoy - tr.date.date()).days
            eventos.append({
                'texto': tr.description,
                'dias_hace': dias
            })

        return Response({
            'piercings_inventario':    piercings_invent,
            'tatuajes_realizados':     tatuajes_realizados,
            'piercings_vendidos':      piercings_vendidos,
            'productos_inventario':    productos_inventario,
            'actividad_reciente':      eventos
        }, status=status.HTTP_200_OK)
