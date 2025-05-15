from django.urls import URLPattern, path, include
from rest_framework.routers import DefaultRouter
from .viewsets import TattooViewSet, PiercingViewSet, ProductoViewSet, Reporte_AbastecimientoViewSet, Reporte_VentaViewSet, Reporte_Uso_MaterialViewSet, ReporteFinanzaViewSet, DashboardAPIView, AuthViewSet

router = DefaultRouter()

router.register('tattoo', TattooViewSet)
router.register('piercing', PiercingViewSet)
router.register('producto', ProductoViewSet)
router.register('reporte_abastecimiento', Reporte_AbastecimientoViewSet)
router.register('reporte_venta', Reporte_VentaViewSet)
router.register('reporte_uso_material', Reporte_Uso_MaterialViewSet)
router.register('reporte_finanza', ReporteFinanzaViewSet)
router.register(r'auth', AuthViewSet, basename='auth')

urlpatterns = [
    path('', include(router.urls)),
    path('dashboard/', DashboardAPIView.as_view(), name='dashboard'),
]