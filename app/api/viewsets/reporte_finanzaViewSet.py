# views.py
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Sum

from app.api.permissions.authentication import CsrfExemptSessionAuthentication
from app.api.permissions.permissions import IsSuperuserOrTatuadorOrPerforador
from ...models import Reporte_Finanza
from app.api.serializers.reporte_finanzaSerializer import Reporte_FinanzaSerializer


class ReporteFinanzaViewSet(viewsets.ReadOnlyModelViewSet):
    """
    /api/finanzas/        -> lista paginada de transacciones
    /api/finanzas/?…      -> filtros por tipo, usuario, búsqueda en descripción
    /api/finanzas/resumen/-> totales (ingresos, gastos, balance)
    """
    queryset         = Reporte_Finanza.objects.all().order_by('-date')
    serializer_class = Reporte_FinanzaSerializer
    filter_backends  = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['transaction_type']
    search_fields    = ['description']
    permission_classes = [IsSuperuserOrTatuadorOrPerforador]
    authentication_classes = [CsrfExemptSessionAuthentication]

    @action(detail=False, methods=['get'])
    def resumen(self, request):
        qs = self.filter_queryset(self.get_queryset())
        tot_ing = qs.filter(transaction_type=Reporte_Finanza.INCOME).aggregate(t=Sum('amount'))['t'] or 0
        tot_gas = qs.filter(transaction_type=Reporte_Finanza.EXPENSE).aggregate(t=Sum('amount'))['t'] or 0
        return Response({
            'total_ingresos': tot_ing,
            'total_gastos':   tot_gas,
            'balance':        tot_ing - tot_gas,
        })
